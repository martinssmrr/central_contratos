from django.urls import path
from . import views
from . import cart_views, checkout_views

app_name = 'contracts'

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/categoria/<slug:slug>/', views.catalog_category_view, name='catalog_category'),
    path('form/<slug:slug>/', views.contract_form_view, name='contract_form'),
    path('payment/<int:contract_id>/', views.payment_page_view, name='payment_page'),
    path('payment/process/<int:contract_id>/', views.process_payment_view, name='process_payment'),
    path('detail/<int:pk>/', views.contract_detail_view, name='contract_detail'),
    path('download/<int:pk>/', views.download_contract_view, name='download_contract'),
    path('my-contracts/', views.user_contracts_view, name='user_contracts'),
    
    # Verificação de status do pagamento
    path('payment/status/<int:contract_id>/', views.payment_status_check, name='payment_status_check'),
    
    # URLs do carrinho de compras
    path('cart/', cart_views.cart_view, name='cart'),
    path('cart/add/<int:contract_id>/', cart_views.cart_add, name='cart_add'),
    path('cart/remove/<int:contract_id>/', cart_views.cart_remove, name='cart_remove'),
    path('cart/clear/', cart_views.cart_clear, name='cart_clear'),
    path('cart/data/', cart_views.get_cart_data, name='cart_data'),
    
    # URLs do checkout
    path('checkout/', checkout_views.checkout_view, name='checkout'),
    path('checkout/success/', checkout_views.checkout_success_view, name='checkout_success'),
    
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
    
    # URLs do Mercado Pago
    path('payment/create/<int:contract_id>/', views.create_payment_preference, name='create_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment-success/', views.payment_success, name='payment_success_auto'),  # Para auto_return
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payment/pending/', views.payment_pending, name='payment_pending'),
    path('payment-pending/', views.payment_pending, name='payment_pending_auto'),  # Para auto_return
    path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
    path('payment/status/<int:contract_id>/', views.payment_status, name='payment_status'),
    path('contract/download/<int:contract_id>/', views.download_contract, name='contract_download'),
    path('contracts/download/<int:contract_id>/', views.download_contract, name='contract_download'),
]
