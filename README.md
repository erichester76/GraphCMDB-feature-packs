# Feature Packs Store

This repository is the feature-pack store used by GraphCMDB.

## How the App Uses This Store
- The app reads `FEATURE_PACK_STORE_REPO` and syncs this repo when the Feature Packs UI loads.
- Installing a pack copies it into the app’s `feature_packs/` directory.
- Uninstalling removes it from `feature_packs/` (the store remains unchanged).

## Packs in This Store
- `audit_log_pack`: Audit log entry type, tabs, and hooks.
- `data_center_pack`: Data center structures (rooms, rows, racks, rack units).
- `dhcp_pack`: DHCP scopes and leases (depends on IPAM).
- `dns_pack`: DNS zones, records, views, and modals.
- `inventory_pack`: Devices and device types (depends on vendor management).
- `ipam_pack`: IPAM networks, IPs, and MACs.
- `itsm_pack`: ITSM objects (issues, changes, problems, releases, events).
- `network_pack`: Interfaces, cables, circuits, VLANs.
- `organization_pack`: Organizations, departments, people, sites, buildings.
- `vendor_management_pack`: Vendors and contracts.
- `virtualization_pack`: Virtual clusters, hosts, VMs.

## Pack Structure (High Level)
- `config.py`: `FEATURE_PACK_CONFIG` metadata (tabs, dependencies, hooks, urls).
- `types.json`: Type definitions that populate the dynamic registry.
- `templates/`: Optional templates and partials used by pack views.
- `views.py`: Optional custom views and modal overrides.
- `hooks.py`: Optional hooks registered via `config.py` for cross-cutting behavior.

## See Also
- `DEVELOPMENT.md` for creating and evolving feature packs.
