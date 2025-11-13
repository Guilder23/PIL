from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('CHOFER', 'Chofer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
