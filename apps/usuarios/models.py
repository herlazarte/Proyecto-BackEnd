from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = [
        ('Cliente', 'Cliente'),
        ('Profesional', 'Profesional')
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    
    # Otros campos específicos de usuario como nombre y email ya están en AbstractUser

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.usuario.username

class Profesional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=255)
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username