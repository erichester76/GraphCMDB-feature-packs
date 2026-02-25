FEATURE_PACK_CONFIG = {
    "name": "Routing Pack",
    "dependencies": [],
    "tabs": [
        {
            "id": "autonomous_system_tab",
            "name": "Autonomous System",
            "template": "routing_pack/autonomous_system_tab.html",
            "for_labels": ["AutonomousSystem"],
            "tab_order": 1
        },
        {
            "id": "bgp_peer_tab",
            "name": "BGP Peer",
            "template": "routing_pack/bgp_peer_tab.html",
            "for_labels": ["BGPPeer"],
            "tab_order": 1
        },
        {
            "id": "bgp_process_tab",
            "name": "BGP Process",
            "template": "routing_pack/bgp_process_tab.html",
            "for_labels": ["BGPProcess"],
            "tab_order": 1
        },
        {
            "id": "ospf_area_tab",
            "name": "OSPF Area",
            "template": "routing_pack/ospf_area_tab.html",
            "for_labels": ["OSPFArea"],
            "tab_order": 1
        },
        {
            "id": "vrf_tab",
            "name": "VRF",
            "template": "routing_pack/vrf_tab.html",
            "for_labels": ["VRF"],
            "tab_order": 1
        },
        {
            "id": "ospf_process_tab",
            "name": "OSPF Process",
            "template": "routing_pack/ospf_process_tab.html",
            "for_labels": ["OSPFProcess"],
            "tab_order": 1
        },
        {
            "id": "isis_process_tab",
            "name": "IS-IS Process",
            "template": "routing_pack/isis_process_tab.html",
            "for_labels": ["IS_ISProcess"],
            "tab_order": 1
        },
        {
            "id": "eigrp_process_tab",
            "name": "EIGRP Process",
            "template": "routing_pack/eigrp_process_tab.html",
            "for_labels": ["EIGRPProcess"],
            "tab_order": 1
        },
        {
            "id": "prefix_list_tab",
            "name": "Prefix List",
            "template": "routing_pack/prefix_list_tab.html",
            "for_labels": ["PrefixList"],
            "tab_order": 1
        },
        {
            "id": "route_map_tab",
            "name": "Route Map",
            "template": "routing_pack/route_map_tab.html",
            "for_labels": ["RouteMap"],
            "tab_order": 1
        },
        {
            "id": "routing_policy_tab",
            "name": "Routing Policy",
            "template": "routing_pack/routing_policy_tab.html",
            "for_labels": ["RoutingPolicy"],
            "tab_order": 1
        },
        {
            "id": "route_target_tab",
            "name": "Route Target",
            "template": "routing_pack/route_target_tab.html",
            "for_labels": ["RouteTarget"],
            "tab_order": 1
        },
        {
            "id": "community_list_tab",
            "name": "Community List",
            "template": "routing_pack/community_list_tab.html",
            "for_labels": ["CommunityList"],
            "tab_order": 1
        }
    ],
}
