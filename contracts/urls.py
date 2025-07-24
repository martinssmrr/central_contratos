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
]
