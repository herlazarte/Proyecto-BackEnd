from django.db import models

# Create your models here.
class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.nombre_servicio } - {self.descripcion}"