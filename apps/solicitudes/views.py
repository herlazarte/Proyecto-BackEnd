from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.solicitudes.models import Solicitud
from django.db.models import Exists, OuterRef, Subquery
from django.db.models import Case, When, Value, CharField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q




from apps.turnos.models import Turno
from apps.usuarios.models import Profesional

class SolicitudesView(LoginRequiredMixin, ListView):
    model = Solicitud
    template_name = 'listado_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        # Obtener el usuario autenticado
        usuario = self.request.user
        
        # Obtener la instancia del Profesional correspondiente al usuario logueado
        try:
            profesional = Profesional.objects.get(usuario=usuario)
        except Profesional.DoesNotExist:
            # Si el usuario no es profesional, simplemente mostramos las solicitudes generales
            return Solicitud.objects.all()
        
        # Filtrar las solicitudes que pertenecen al profesional logueado o no tienen turno asignado
        solicitudes = Solicitud.objects.filter(
            Q(turno__profesional=profesional) | Q(turno=None)
        ).annotate(
            turno_asignado=Exists(Turno.objects.filter(solicitud=OuterRef('pk'), profesional=profesional)),
            estado_turno=Subquery(
                Turno.objects.filter(solicitud=OuterRef('pk'), profesional=profesional).values('estado')[:1]
            )
        )
        
        return solicitudes

class SolicitudesClienteView(TemplateView):
    template_name = "dashboard_cliente.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Obtener el objeto cliente asociado con el usuario actual
        cliente = self.request.user.cliente
        # Filtrar las solicitudes según el cliente
        contexto['solicitudes'] = Solicitud.objects.filter(cliente=cliente)
        return contexto
