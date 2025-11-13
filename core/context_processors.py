from django.urls import reverse
from .models import PerfilUsuario, SidebarPermission
from .menus import MENU_DEFS


def sidebar_items(request):
    items = []
    # Siempre mostrar Inicio
    try:
        items.append({"label": "Inicio", "href": reverse("home")})
    except Exception:
        pass

    role = None
    if getattr(request, "user", None) and request.user.is_authenticated:
        perfil = getattr(request.user, "perfil", None)
        role = getattr(perfil, "role", None)

    # Dashboard según rol (o genérico si no hay rol)
    try:
        if role == PerfilUsuario.ADMIN:
            items.append({"label": "Dashboard", "href": reverse("dashboard_admin")})
        elif role == PerfilUsuario.CLIENTE:
            items.append({"label": "Dashboard", "href": reverse("dashboard_cliente")})
        elif role == PerfilUsuario.CHOFER:
            items.append({"label": "Dashboard", "href": reverse("dashboard_chofer")})
        else:
            items.append({"label": "Dashboard", "href": reverse("dashboard")})
    except Exception:
        # Si no existe alguna ruta, no romper el render
        pass

    # Ítems dinámicos según permisos persistidos
    if role in MENU_DEFS:
        defs = MENU_DEFS[role]
        for d in defs:
            perm = SidebarPermission.objects.filter(role=role, key=d['key']).first()
            enabled = perm.enabled if perm is not None else True
            if enabled:
                href = None
                if 'url_name' in d:
                    try:
                        href = reverse(d['url_name'])
                    except Exception:
                        href = d.get('href', '#')
                else:
                    href = d.get('href', '#')
                items.append({ 'label': d['label'], 'href': href })

    return {"sidebar_items": items}