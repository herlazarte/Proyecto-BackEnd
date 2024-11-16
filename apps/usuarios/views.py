from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, CreateView
from apps.servicios.models import Servicio
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud
from apps.usuarios.forms import SolicitudForm
from apps.servicios.forms import ServicioForm
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
    
########## ABM SOLICITUDES ############
class CrearSolicitudView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "crear_solicitud.html"
    success_url = "/crear_solicitud/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasar el usuario logueado al formulario
        return kwargs

    def form_valid(self, form):
        # Crear el servicio con los datos del formulario
        nombre_servicio = form.cleaned_data['nombre_servicio']
        descripcion_servicio = form.cleaned_data['descripcion_servicio']
        servicio = Servicio.objects.create(nombre_servicio=nombre_servicio, descripcion=descripcion_servicio)

        # Asignar el cliente al formulario de solicitud
        user_cliente = self.request.user.cliente
        if not user_cliente:
            return redirect('/error_cliente_no_asociado/')

        # Asignar el servicio recién creado a la solicitud
        form.instance.cliente = user_cliente
        form.instance.servicio = servicio

        return super().form_valid(form)


########## ABM SOLICITUDES ############
class HomeView(TemplateView):
    template_name = "base.html"
