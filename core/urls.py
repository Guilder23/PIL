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

    # Permisos de sidebar (solo ADMIN)
    path('permisos/', views.permisos_sidebar, name='permisos_sidebar'),
    path('inventario/', views.inventario_dashboard, name='inventario_dashboard'),
    path('inventario/productos/', views.productos_list, name='productos_list'),
    path('inventario/productos/nuevo/', views.producto_create, name='producto_create'),
    path('inventario/productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('inventario/productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

    path('inventario/movimientos/', views.movimientos_list, name='movimientos_list'),
    path('inventario/movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
    path('inventario/movimientos/entrada/', views.movimiento_create, { 'tipo': 'ENTRADA' }, name='movimiento_entrada'),
    path('inventario/movimientos/salida/', views.movimiento_create, { 'tipo': 'SALIDA' }, name='movimiento_salida'),
    path('inventario/movimientos/ajuste/', views.movimiento_create, { 'tipo': 'AJUSTE' }, name='movimiento_ajuste'),

    path('inventario/disponible/', views.inventario_disponible, name='inventario_disponible'),
]