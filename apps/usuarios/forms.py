from django import forms
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'rol']

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['cliente', 'servicio', 'fecha_servicio']

# class ClienteForm(forms.ModelForm):
#     class Meta:
#         model = Cliente
#         fields = ['usuario', 'direccion', 'telefono']