from django.contrib import admin
from .models import PerfilUsuario

# Register your models here.

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'user__email')
    list_filter = ('role',)
