from django import forms
from apps.solicitudes.models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['cliente', 'servicio', 'fecha_servicio', 'estado']