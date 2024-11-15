from django.contrib import admin
from .models import Usuario, Profesional, Cliente


# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'disponibilidad')
    list_filter = ('especialidad', 'disponibilidad')
    search_fields = ('usuario__username', 'especialidad')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'direccion', 'telefono')
    search_fields = ('usuario__username', 'direccion', 'telefono')
    list_filter = ('direccion', 'telefono')
