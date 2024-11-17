from django.db import models
from django.conf import settings
from apps.servicios.models import Servicio
from apps.usuarios.models import Cliente

class Solicitud(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_servicio = models.DateField()
    estado = models.CharField(max_length=10, default='Pendiente')

    def __str__(self):
        return f"{self.cliente}"