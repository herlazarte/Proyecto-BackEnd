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
