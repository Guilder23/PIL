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

    # Gestión de usuarios (solo ADMIN)
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/nuevo/', views.usuarios_create, name='usuarios_create'),
    path('usuarios/<int:user_id>/editar/', views.usuarios_update, name='usuarios_update'),
    path('usuarios/<int:user_id>/eliminar/', views.usuarios_delete, name='usuarios_delete'),
    path('usuarios/<int:user_id>/password/', views.usuarios_change_password, name='usuarios_change_password'),
]