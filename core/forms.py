from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .models import Producto, InventarioMovimiento

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=PerfilUsuario.ROLE_CHOICES, label='Rol')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            PerfilUsuario.objects.create(user=user, role=self.cleaned_data['role'])
        return user

class AdminUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=PerfilUsuario.ROLE_CHOICES)
    is_active = forms.BooleanField(required=False, initial=True, label='Activo')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_active")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = self.cleaned_data.get("is_active", True)
        if commit:
            user.save()
            PerfilUsuario.objects.create(user=user, role=self.cleaned_data["role"])
        return user

class AdminUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=PerfilUsuario.ROLE_CHOICES)
    is_active = forms.BooleanField(required=False, label='Activo')

    class Meta:
        model = User
        fields = ("username", "email", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')
        if user:
            perfil = getattr(user, 'perfil', None)
            self.fields['role'].initial = getattr(perfil, 'role', PerfilUsuario.CLIENTE)

    def save(self, commit=True):
        user = super().save(commit=commit)
        perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
        perfil.role = self.cleaned_data['role']
        perfil.save()
        return user

class AdminUserPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Nueva contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned


class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "categoria", "unidad_medida", "activo", "stock"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.TextInput(attrs={"class": "form-control"}),
            "unidad_medida": forms.TextInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = InventarioMovimiento
        fields = ["producto", "tipo", "cantidad", "referencia", "nota"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "referencia": forms.TextInput(attrs={"class": "form-control"}),
            "nota": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }