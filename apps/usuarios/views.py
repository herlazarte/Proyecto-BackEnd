from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, CreateView
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud
from apps.usuarios.forms import SolicitudForm
from apps.usuarios.forms import UsuarioForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin




# Create your views here.
class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard_cliente.html'
    
    #solo ingresa a la vista los que tienen el rol de cliente
    def test_func(self):
        return self.request.user.rol == 'Cliente'

    
    
class AltaClientesView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "alta_cliente.html"
    success_url = "/alta_cliente/"

class CrearSolicitudView(CreateView):
    template_name = 'crear_solicitud.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SolicitudForm(user=self.request.user)  # Pasar el usuario actual
        context['form'] = form
        return context
    


class HomeView(TemplateView):
    template_name = "base.html"
