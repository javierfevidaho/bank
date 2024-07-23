from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]

handler404 = 'core.views.error_404'  # Assuming 'error_404' view exists in core/views.py
