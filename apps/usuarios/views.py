from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, CreateView
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud
from apps.usuarios.forms import SolicitudForm
from apps.usuarios.forms import UsuarioForm, ClienteForm
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
    template_name = 'alta_cliente.html'
    form_class = UsuarioForm
    success_url = '/alta_cliente/'  # Puedes redirigir a la página de inicio o donde desees

    def get_context_data(self, **kwargs):
        # Añadir el formulario de Cliente al contexto
        context = super().get_context_data(**kwargs)
        context['cliente_form'] = ClienteForm()  # Añadir formulario de Cliente
        return context

    def form_valid(self, form):
        # Guardar el Usuario
        usuario = form.save()

        # Crear el Cliente y asociarlo con el Usuario
        cliente_form = ClienteForm(self.request.POST)
        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.usuario = usuario  # Asociar el Usuario con el Cliente
            cliente.save()

        # Iniciar sesión con el Usuario creado
        login(self.request, usuario)

        return super().form_valid(form)
    

class CrearSolicitudView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "crear_solicitud.html"
    success_url = "/crear_solicitud/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SolicitudForm(user=self.request.user)  # Pasar el usuario logueado
        return context

    def form_valid(self, form):
        # Asignar el cliente (asumiendo que el usuario tiene un cliente relacionado)
        user_cliente = self.request.user.cliente  # Obtener el cliente asociado al usuario logueado
        if user_cliente:  # Verificar si el usuario tiene un cliente relacionado
            form.instance.cliente = user_cliente  # Asignar el cliente al formulario
        else:
            # Si el usuario no tiene un cliente asociado, redirigir a otro lugar o mostrar un mensaje de error
            return redirect('/error_cliente_no_asociado/')

        return super().form_valid(form)


class HomeView(TemplateView):
    template_name = "base.html"
