from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

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


class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=100, blank=True)
    unidad_medida = models.CharField(max_length=20, default="unidad")
    activo = models.BooleanField(default=True)
    stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre} ({self.stock} {self.unidad_medida})"


class InventarioMovimiento(models.Model):
    TIPO_CHOICES = (
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
        ("AJUSTE", "Ajuste"),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=100, blank=True)  # por ejemplo id de pedido
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo} {self.cantidad} de {self.producto.nombre}"

    def clean(self):
        # Evitar cantidades cero o negativas (excepto AJUSTE puede ser negativa para reducir)
        if self.tipo in ("ENTRADA", "SALIDA") and self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser positiva para entradas y salidas.")
        if self.tipo == "AJUSTE" and self.cantidad == 0:
            raise ValidationError("La cantidad de ajuste no puede ser cero.")

    def save(self, *args, **kwargs):
        is_create = self.pk is None
        super().save(*args, **kwargs)
        # Ajuste de stock: aplicar sólo en creación para no duplicar
        if is_create:
            prod = self.producto
            if self.tipo == "ENTRADA":
                prod.stock = (prod.stock or 0) + self.cantidad
            elif self.tipo == "SALIDA":
                nueva = (prod.stock or 0) - self.cantidad
                if nueva < 0:
                    # revertir registro si dejaría stock negativo
                    super().delete()
                    raise ValidationError("Stock insuficiente para salida.")
                prod.stock = nueva
            elif self.tipo == "AJUSTE":
                nueva = (prod.stock or 0) + self.cantidad
                if nueva < 0:
                    super().delete()
                    raise ValidationError("El ajuste dejaría stock negativo.")
                prod.stock = nueva
            prod.save(update_fields=["stock"])
