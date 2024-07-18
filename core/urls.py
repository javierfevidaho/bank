from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('purchase_ticket/', views.purchase_ticket, name='purchase_ticket'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('coinbase-payment/', views.coinbase_payment, name='coinbase_payment'),
]