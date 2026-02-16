# Feature Pack Development

This guide explains how to build and extend GraphCMDB feature packs.

## Pack Layout
A typical pack has the following structure:

```
my_pack/
  config.py
  types.json
  views.py              # optional
  hooks.py              # optional
  urls.py               # optional
  templates/
    ...
```

### `config.py`
Define `FEATURE_PACK_CONFIG` with pack metadata:

```python
FEATURE_PACK_CONFIG = {
    "name": "My Pack",
    "dependencies": ["organization_pack"],
    "tabs": [
        {
            "id": "my_tab",
            "name": "My Tab",
            "template": "my_tab.html",
            "custom_view": "my_pack.views.my_tab",
            "for_labels": ["MyType"],
            "tab_order": 10
        }
    ],
    "modals": [
        {
            "type": "create",
            "template": "my_create_modal.html",
            "custom_view": "my_pack.views.my_create_modal",
            "for_labels": ["MyType"]
        }
    ],
    "hooks": {
        "audit": "audit_log_pack.hooks.register_hooks"
    },
    "urls": {
        "prefix": "",
        "module": "my_pack.urls"
    }
}
```

- **`dependencies`**: pack names that must be installed/enabled first.
- **`tabs`**: add UI tabs per label.
- **`modals`**: override create/edit modals for specific labels.
- **`hooks`**: register hooks (e.g., audit) via a callable path.
- **`urls`**: optionally expose routes; these are dynamically included by the app.

### `types.json`
Defines dynamic node types and metadata.

```json
{
  "MyType": {
    "display_name": "My Type",
    "category": "Custom",
    "properties": ["name", "status"],
    "required": ["name"],
    "relationships": {
      "RELATED_TO": {
        "target": "OtherType",
        "direction": "out"
      }
    }
  }
}
```

### `views.py` (optional)
Use custom views for tabs, modals, or API-like functionality. Keep views focused on pack-specific behavior. Prefer shared core helpers for audit logging and validation.

### `hooks.py` (optional)
Hooks let packs register cross-cutting logic. For example, audit logging hooks are registered via `FEATURE_PACK_CONFIG["hooks"]`.

### `urls.py` (optional)
Expose pack routes. Example:

```python
from django.urls import path
from . import views

app_name = "my_pack"

urlpatterns = [
    path("my-pack/", views.my_pack_list, name="my_pack_list"),
]
```

## How Packs Are Loaded
On startup (and on reload), the app:
1. Scans `feature_packs/`
2. Loads `config.py` and `types.json`
3. Registers types in the dynamic registry
4. Adds templates to Django’s template search path
5. Registers tabs and modal overrides
6. Registers hooks and URLs declared in config

## Audit Logging (Hooks)
Pack code should **not** import `audit_log_pack` directly. Instead:

- Emit events via `cmdb.audit_hooks.emit_audit(...)`.
- The audit pack registers a hook so events are stored when enabled.

If you want a helper, use `cmdb.audit_helpers.audit_create_node` and `audit_update_node`.

## Dependencies
Dependencies are enforced at install time. If a dependency pack is missing or disabled, installation is blocked and the UI shows an error.

## Testing Packs
- Install the pack via Feature Packs UI.
- Confirm types appear in the sidebar and registry.
- Validate templates and modals render.
- Verify hooks fire (audit entries appear).

## Packaging Tips
- Keep views thin; reuse shared helpers for validation and audit.
- Avoid direct imports from other packs where possible.
- Use `config.py` for all registrations (tabs, modals, hooks, urls).
