from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud
from apps.usuarios.forms import SolicitudForm
from apps.usuarios.forms import UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class DashboardView(TemplateView):
    template_name = "dashboard_cliente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = Usuario.objects.filter(rol='Cliente')
        user = self.request.user
        context['is_active'] = user.is_active
        context['is_staff'] = user.is_staff
        return context
    
class AltaClientesView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "alta_cliente.html"
    success_url = "/alta_cliente/"

class CrearSolicitudView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "crear_solicitud.html"
    success_url = "/crear_solicitud/"
    


class HomeView(TemplateView):
    template_name = "base.html"
