from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('form/<slug:slug>/', views.contract_form_view, name='contract_form'),
    path('payment/<int:contract_id>/', views.payment_view, name='payment'),
    path('detail/<int:pk>/', views.contract_detail_view, name='contract_detail'),
    path('download/<int:pk>/', views.download_contract_view, name='download_contract'),
    path('my-contracts/', views.user_contracts_view, name='user_contracts'),
    
    # URLs específicas para compra e venda de imóvel
    path('compra-venda-imovel/', views.compra_venda_imovel_view, name='compra_venda_imovel'),
    path('compra-venda-sucesso/<int:pk>/', views.compra_venda_success_view, name='compra_venda_success'),
    path('compra-venda-detalhes/<int:pk>/', views.compra_venda_detail_view, name='compra_venda_detail'),
    path('meus-contratos-compra-venda/', views.meus_contratos_compra_venda_view, name='meus_contratos_compra_venda'),
    
    # URLs para o formulário completo de compra e venda
    path('compra-venda-completo/', views.contrato_compra_venda_completo_view, name='compra_venda_completo'),
    path('compra-venda-completo-detalhes/<int:pk>/', views.compra_venda_detail_completo_view, name='compra_venda_detail_completo'),
    path('compra-venda-completo-sucesso/<int:pk>/', views.compra_venda_success_completo_view, name='compra_venda_success_completo'),
    
    # URLs para locação residencial
    path('locacao-residencial/', views.locacao_residencial_view, name='locacao_residencial'),
    path('locacao-residencial-detalhes/<int:pk>/', views.locacao_residencial_detail_view, name='locacao_residencial_detail'),
    path('locacao-residencial-sucesso/<int:pk>/', views.locacao_residencial_success_view, name='locacao_residencial_success'),
    path('meus-contratos-locacao-residencial/', views.meus_contratos_locacao_residencial_view, name='meus_contratos_locacao_residencial'),
]
