from django.urls import path
from . import views

app_name = 'audit_log_pack'

urlpatterns = [
    path('audit-log/', views.audit_log_list, name='audit_log_list'),
    path('audit-log/<str:entry_id>/revert/', views.audit_log_revert, name='audit_log_revert'),
]
