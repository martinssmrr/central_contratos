from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('painel/', views.admin_panel_view, name='admin_panel'),
    path('contratos/', views.contracts_management_view, name='contracts_management'),
    path('tipos-contrato/', views.contract_types_management_view, name='contract_types_management'),
    
    # Teste
    path('teste/', views.test_view, name='test'),
    
    # CRUD de Tipos de Contrato
    path('crud-tipos/', views.contract_types_crud_view, name='contract_types_crud'),
    path('criar-tipo/', views.contract_type_create_view, name='contract_type_create'),
    path('editar-tipo/<int:contract_type_id>/', views.contract_type_edit_view, name='contract_type_edit'),
    path('excluir-tipo/<int:contract_type_id>/', views.contract_type_delete_view, name='contract_type_delete'),
    path('contract-types/<int:contract_type_id>/data/', views.contract_type_data_view, name='contract_type_data'),
    
    # AJAX
    path('ajax/update-contract-type/', views.update_contract_type_ajax, name='update_contract_type_ajax'),
    path('ajax/quick-edit-contract-type/', views.contract_type_quick_edit_ajax, name='contract_type_quick_edit_ajax'),
    path('ajax/get-contract-type/<int:contract_type_id>/', views.get_contract_type_ajax, name='get_contract_type_ajax'),
    
    path('contrato/<int:contract_id>/', views.contract_detail_admin_view, name='contract_detail_admin'),
    path('contracts/', views.contracts_report_view, name='contracts_report'),
    path('payments/', views.payments_report_view, name='payments_report'),
    path('users/', views.users_report_view, name='users_report'),
]
