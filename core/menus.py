from typing import Dict, List

MENU_DEFS: Dict[str, List[dict]] = {
    'ADMIN': [
        { 'key': 'dashboard_admin', 'label': 'Dashboard', 'url_name': 'dashboard_admin' },
        { 'key': 'usuarios', 'label': 'Gestión de Usuarios', 'url_name': 'usuarios_list' },
        { 'key': 'permisos_sidebar', 'label': 'Permisos del Sidebar', 'url_name': 'permisos_sidebar' },
        { 'key': 'inventario', 'label': 'Inventario', 'url_name': 'inventario_dashboard' },
        { 'key': 'pedidos', 'label': 'Pedidos', 'href': '#' },
        { 'key': 'rutas', 'label': 'Rutas', 'href': '#' },
        { 'key': 'reportes', 'label': 'Reportes', 'href': '#' },
        # Opciones del Cliente visibles también para ADMIN
        { 'key': 'realizar_pedido', 'label': 'Realizar Pedido', 'href': '#' },
        { 'key': 'inventario_disponible', 'label': 'Inventario disponible', 'url_name': 'inventario_disponible' },
        { 'key': 'pagos', 'label': 'Pagos', 'href': '#' },
        { 'key': 'historial', 'label': 'Historial', 'href': '#' },
        { 'key': 'reportar_entrega', 'label': 'Reportar entrega', 'href': '#' },
        # Opciones del Chofer visibles también para ADMIN
        { 'key': 'pedidos_asignados', 'label': 'Pedidos asignados', 'href': '#' },
        { 'key': 'ruta_automatica', 'label': 'Ruta automática', 'href': '#' },
        { 'key': 'confirmar_entrega', 'label': 'Confirmar entrega', 'href': '#' },
        { 'key': 'evidencias', 'label': 'Evidencias', 'href': '#' },
        { 'key': 'reportes_clientes', 'label': 'Reportes de clientes', 'href': '#' },
    ],
    'CLIENTE': [
        { 'key': 'dashboard_cliente', 'label': 'Dashboard', 'url_name': 'dashboard_cliente' },
        { 'key': 'realizar_pedido', 'label': 'Realizar Pedido', 'href': '#' },
        { 'key': 'inventario_disponible', 'label': 'Inventario disponible', 'href': '#' },
        { 'key': 'pagos', 'label': 'Pagos', 'href': '#' },
        { 'key': 'historial', 'label': 'Historial', 'href': '#' },
        { 'key': 'reportar_entrega', 'label': 'Reportar entrega', 'href': '#' },
    ],
    'CHOFER': [
        { 'key': 'dashboard_chofer', 'label': 'Dashboard', 'url_name': 'dashboard_chofer' },
        { 'key': 'pedidos_asignados', 'label': 'Pedidos asignados', 'href': '#' },
        { 'key': 'ruta_automatica', 'label': 'Ruta automática', 'href': '#' },
        { 'key': 'confirmar_entrega', 'label': 'Confirmar entrega', 'href': '#' },
        { 'key': 'evidencias', 'label': 'Evidencias', 'href': '#' },
        { 'key': 'reportes_clientes', 'label': 'Reportes de clientes', 'href': '#' },
    ],
}