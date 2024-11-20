from django.shortcuts import render
from django.views.generic import TemplateView

from apps.solicitudes.models import Solicitud
# Create your views here.

class SolicitudesView(TemplateView):
    template_name = "listado_solicitudes.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitudes'] = Solicitud.objects.all()
        return context

class SolicitudesClienteView(TemplateView):
    template_name = "dashboard_cliente.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Obtener el objeto cliente asociado con el usuario actual
        cliente = self.request.user.cliente
        # Filtrar las solicitudes según el cliente
        contexto['solicitudes'] = Solicitud.objects.filter(cliente=cliente)
        return contexto
