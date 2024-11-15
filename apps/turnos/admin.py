from django.contrib import admin
from apps.turnos.models import Turno
# Register your models here.
@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('profesional', 'solicitud', 'estado', 'fecha_turno')
    search_fields = ('profesional__usuario__username', 'solicitud__cliente__usuario__username', 'estado', 'fecha_turno')
    list_filter = ('profesional', 'solicitud', 'estado', 'fecha_turno')