from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from apps.usuarios.models import Cliente, Usuario
from apps.usuarios.forms import UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class AltaClientesView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "alta_cliente.html"
    success_url = "/alta_cliente/"

class DashboardView(TemplateView):
    template_name = "dashboard_cliente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = Usuario.objects.filter(rol='Cliente')
        return context

class HomeView(TemplateView):
    template_name = "base.html"
