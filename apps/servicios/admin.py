from django.contrib import admin
from apps.servicios.models import Servicio

# Register your models here.
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'descripcion')
    search_fields = ('nombre_servicio', 'descripcion')
    list_filter = ('nombre_servicio', 'descripcion')

