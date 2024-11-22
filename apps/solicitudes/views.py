from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.solicitudes.models import Solicitud
from django.db.models import Exists, OuterRef, Subquery
from django.db.models import Case, When, Value, CharField


from apps.turnos.models import Turno

# Create your views here.

class SolicitudesView(ListView):
    model = Solicitud
    template_name = 'listado_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        # Agregar el campo 'turno_asignado' y 'estado_turno' a cada solicitud
        return Solicitud.objects.annotate(
            turno_asignado=Exists(Turno.objects.filter(solicitud=OuterRef('pk'))),
            estado_turno=Subquery(
                Turno.objects.filter(solicitud=OuterRef('pk')).values('estado')[:1]
            )
        )

class SolicitudesClienteView(TemplateView):
    template_name = "dashboard_cliente.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Obtener el objeto cliente asociado con el usuario actual
        cliente = self.request.user.cliente
        # Filtrar las solicitudes según el cliente
        contexto['solicitudes'] = Solicitud.objects.filter(cliente=cliente)
        return contexto
