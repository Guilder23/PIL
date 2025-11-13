from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.registro, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/chofer/', views.dashboard_chofer, name='dashboard_chofer'),
]