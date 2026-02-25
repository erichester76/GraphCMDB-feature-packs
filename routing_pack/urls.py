from django.urls import path
from . import views

app_name = "routing_pack"

urlpatterns = [
    path('autonomous-systems/', views.autonomous_system_list, name='autonomous_system_list'),
    path('bgp-peers/', views.bgp_peer_list, name='bgp_peer_list'),
    path('bgp-processes/', views.bgp_process_list, name='bgp_process_list'),
    path('ospf-areas/', views.ospf_area_list, name='ospf_area_list'),
    path('vrfs/', views.vrf_list, name='vrf_list'),
    path('ospf-processes/', views.ospf_process_list, name='ospf_process_list'),
    path('isis-processes/', views.isis_process_list, name='isis_process_list'),
    path('eigrp-processes/', views.eigrp_process_list, name='eigrp_process_list'),
    path('prefix-lists/', views.prefix_list_list, name='prefix_list_list'),
    path('route-maps/', views.route_map_list, name='route_map_list'),
    path('routing-policies/', views.routing_policy_list, name='routing_policy_list'),
    path('route-targets/', views.route_target_list, name='route_target_list'),
    path('community-lists/', views.community_list_list, name='community_list_list'),
]
