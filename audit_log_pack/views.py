# feature_packs/audit_log_pack/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
import json
from cmdb.audit_hooks import emit_audit
from cmdb.registry import TypeRegistry
from users.views import has_node_permission
from neomodel import db
from cmdb.models import DynamicNode


def audit_log_tab(request, label, element_id):
    """
    Custom view for Audit Log tab on node detail pages.
    Shows audit log entries filtered to the specific node.
    """
    context = {
        'label': label,
        'element_id': element_id,
        'custom_data': {
            'audit_entries': []
        },
        'error': None,
    }

    try:
        # Fetch all audit log entries using neomodel (same as global view)
        audit_node_class = DynamicNode.get_or_create_label('AuditLogEntry')
        all_audit_nodes = audit_node_class.nodes.all()
        
        # Filter to only entries for this specific node and extract properties
        audit_entries = []
        def normalize_props(value):
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return {}
            return value or {}

        for node in all_audit_nodes:
            props = node.custom_properties or {}
            # Filter by node_id matching the element_id
            if props.get('node_id') == element_id:
                old_props = normalize_props(props.get('old_props'))
                new_props = normalize_props(props.get('new_props'))
                audit_entries.append({
                    'id': node.element_id,
                    'timestamp': props.get('timestamp', ''),
                    'action': props.get('action', ''),
                    'node_label': props.get('node_label', ''),
                    'node_name': props.get('node_name', 'Unknown'),
                    'user': props.get('user', 'System'),
                    'changes': props.get('changes', ''),
                    'relationship_type': props.get('relationship_type', ''),
                    'target_label': props.get('target_label', ''),
                    'target_id': props.get('target_id', ''),
                    'old_props': old_props,
                    'new_props': new_props,
                    'old_props_json': json.dumps(old_props, indent=2, sort_keys=True) if old_props else '',
                    'new_props_json': json.dumps(new_props, indent=2, sort_keys=True) if new_props else ''
                })
        
        # Sort by timestamp descending (most recent first) and limit to 100
        audit_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        context['custom_data']['audit_entries'] = audit_entries[:100]

    except Exception as e:
        context['error'] = str(e)

    return context


def _normalize_props(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}
    return value or {}


@require_http_methods(["GET"])
def audit_log_list(request):
    """
    Global audit log view showing all audit log entries across all nodes.
    Supports HTMX partial updates
    """
    try:
        audit_node_class = DynamicNode.get_or_create_label('AuditLogEntry')
        audit_nodes = audit_node_class.nodes.all()[:200]

        audit_entries = []
        for node in audit_nodes:
            props = node.custom_properties or {}
            old_props = _normalize_props(props.get('old_props'))
            new_props = _normalize_props(props.get('new_props'))
            audit_entries.append({
                'element_id': node.element_id,
                'timestamp': props.get('timestamp', ''),
                'action': props.get('action', ''),
                'node_label': props.get('node_label', ''),
                'node_id': props.get('node_id', ''),
                'node_name': props.get('node_name', 'Unknown'),
                'user': props.get('user', 'System'),
                'changes': props.get('changes', ''),
                'relationship_type': props.get('relationship_type', ''),
                'target_label': props.get('target_label', ''),
                'target_id': props.get('target_id', ''),
                'old_props': old_props,
                'new_props': new_props,
                'old_props_json': json.dumps(old_props, indent=2, sort_keys=True) if old_props else '',
                'new_props_json': json.dumps(new_props, indent=2, sort_keys=True) if new_props else ''
            })

        audit_entries.sort(key=lambda x: x['timestamp'], reverse=True)

    except Exception as exc:
        print(f"Error fetching audit log: {exc}")
        audit_entries = []

    context = {
        'audit_entries': audit_entries,
        'all_labels': TypeRegistry.known_labels(),
    }

    if request.htmx:
        content_html = render_to_string('audit_log_pack/partials/audit_log_content.html', context, request=request)
        header_html = render_to_string('audit_log_pack/partials/audit_log_header.html', context, request=request)
        return HttpResponse(content_html + header_html)

    return render(request, 'audit_log_pack/audit_log_list.html', context)


@require_http_methods(["POST"])
@login_required
def audit_log_revert(request, entry_id):
    try:
        audit_node_class = DynamicNode.get_or_create_label('AuditLogEntry')
        audit_entry = audit_node_class.get_by_element_id(entry_id)
        if not audit_entry:
            messages.error(request, 'Audit log entry not found.')
            return redirect('audit_log_pack:audit_log_list')

        props = audit_entry.custom_properties or {}
        node_label = props.get('node_label')
        node_id = props.get('node_id')
        old_props = props.get('old_props') or {}
        if isinstance(old_props, str):
            try:
                old_props = json.loads(old_props)
            except json.JSONDecodeError:
                old_props = {}

        if not node_label or not node_id:
            messages.error(request, 'Audit log entry is missing node information.')
            return redirect('audit_log_pack:audit_log_list')

        if not old_props:
            messages.error(request, 'No previous values stored for this audit entry.')
            return redirect('audit_log_pack:audit_log_list')

        if not has_node_permission(request.user, 'change', node_label):
            messages.error(request, 'Access Denied: insufficient permissions to revert.')
            return redirect('audit_log_pack:audit_log_list')

        node_class = DynamicNode.get_or_create_label(node_label)
        node = node_class.get_by_element_id(node_id)
        if not node:
            messages.error(request, 'Target node not found.')
            return redirect('audit_log_pack:audit_log_list')

        node.custom_properties = old_props
        node.save()

        emit_audit(
            action='revert',
            node_label=node_label,
            node_id=node_id,
            node_name=old_props.get('name', ''),
            user=request.user.username if request.user.is_authenticated else 'System',
            changes='Reverted to previous values'
        )

        messages.success(request, 'Reverted to previous values.')
        return redirect('audit_log_pack:audit_log_list')
    except Exception as exc:
        messages.error(request, f'Failed to revert: {exc}')
        return redirect('audit_log_pack:audit_log_list')


