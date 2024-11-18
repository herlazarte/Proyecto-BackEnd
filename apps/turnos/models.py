from django.db import models
from apps.solicitudes.models import Solicitud
from apps.usuarios.models import Profesional

class Turno(models.Model):
    ESTADO_CHOICES = [
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado')
    ]

    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    fecha_turno = models.DateField()

    def __str__(self):
        return f"{self.profesional} - {self.solicitud}"