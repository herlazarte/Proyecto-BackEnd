
from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['estado', 'fecha_turno']
        labels = {
            'estado': 'Estado',
            'fecha_turno': 'Fecha del Turno'
        }
        widgets = {
            'fecha_turno': forms.DateInput(attrs={'type': 'date'})
        }
                
