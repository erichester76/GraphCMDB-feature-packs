from datetime import datetime, timezone
from cmdb.models import DynamicNode
from cmdb.registry import TypeRegistry


def create_audit_entry(action, node_label, node_id, node_name=None, user=None, changes=None,
                       relationship_type=None, target_label=None, target_id=None,
                       old_props=None, new_props=None):
    if 'AuditLogEntry' not in TypeRegistry.known_labels():
        return None

    try:
        audit_node_class = DynamicNode.get_or_create_label('AuditLogEntry')
        properties = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'action': action,
            'node_label': node_label,
            'node_id': node_id,
            'node_name': node_name or '',
            'user': user or 'System',
            'changes': changes or '',
            'relationship_type': relationship_type or '',
            'target_label': target_label or '',
            'target_id': target_id or ''
        }
        if old_props is not None:
            properties['old_props'] = old_props
        if new_props is not None:
            properties['new_props'] = new_props
        return audit_node_class(custom_properties=properties).save()
    except Exception as exc:
        print(f"Error creating audit log entry: {exc}")
        return None


def register_hooks(register_audit_hook):
    register_audit_hook(create_audit_entry)
