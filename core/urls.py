from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.http import HttpResponse


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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),  # Incluye las rutas de autenticación de Django, incluyendo restablecimiento de contraseña
    path('guest-login/', views.guest_login, name='guest_login'),
    path('winners/', views.winners, name='winners'),
    path('winning_numbers/', views.winning_numbers, name='winning_numbers'),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="static/robots.txt", content_type="text/plain")),
    path('api/get-balance/', views.get_balance, name='get_balance'),
    path('realizar-sorteo/', views.realizar_sorteo, name='realizar_sorteo'),
    path('favicon.ico', RedirectView.as_view(url=static('path/to/your/favicon.ico'), permanent=True)),
    path("robots.txt", views.robots_txt, name="robots_txt"),

]
