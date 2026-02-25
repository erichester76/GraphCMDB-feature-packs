# Routing Pack

This feature pack manages routing concepts such as BGP peers, OSPF areas, and VRFs for GraphCMDB.

## Structure
- config.py: Declares FEATURE_PACK_CONFIG with tabs and URLs
- types.json: Defines BGPPeer, OSPFArea, VRF types
- templates/: Tab templates for each type
- views.py, urls.py: (Optional) For custom logic

## Usage
- Install via Feature Packs UI
- Types will appear in the sidebar and registry
- Tabs will render for each type

See DEVELOPMENT.md for extension and integration details.
