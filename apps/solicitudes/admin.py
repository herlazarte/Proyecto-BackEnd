from django.contrib import admin
from apps.solicitudes.models import Solicitud

# Register your models here.
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'fecha_solicitud', 'fecha_servicio', 'estado')
    search_fields = ('cliente__usuario__username', 'servicio__nombre_servicio', 'fecha_solicitud', 'fecha_servicio', 'estado')
    list_filter = ('cliente', 'servicio', 'fecha_solicitud', 'fecha_servicio', 'estado')