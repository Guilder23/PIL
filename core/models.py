from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    ADMIN = 'ADMIN'
    CLIENTE = 'CLIENTE'
    CHOFER = 'CHOFER'

    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (CHOFER, 'Chofer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class SidebarPermission(models.Model):
    role = models.CharField(max_length=10, choices=PerfilUsuario.ROLE_CHOICES)
    key = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'key')

    def __str__(self):
        return f"{self.role}:{self.key}={'on' if self.enabled else 'off'}"
