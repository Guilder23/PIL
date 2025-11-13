from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

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