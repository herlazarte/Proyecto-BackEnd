from django import forms
from apps.usuarios.models import Cliente, Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'rol']


# class ClienteForm(forms.ModelForm):
#     class Meta:
#         model = Cliente
#         fields = ['usuario', 'direccion', 'telefono']