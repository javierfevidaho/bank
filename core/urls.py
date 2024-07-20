from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('deposit/', views.deposit, name='deposit'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('purchase-ticket/', views.purchase_ticket, name='purchase_ticket'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('coinbase-payment/', views.coinbase_payment, name='coinbase_payment'),
    path('payment/', views.payment, name='payment'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('api-login/', views.api_login, name='api_login'),
]
