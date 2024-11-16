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
    template_name = "crear_solicitud.html"
    form_class = SolicitudForm
    success_url = "/crear_solicitud/"

    def get_context_data(self, **kwargs):
        # Añadir el formulario de Servicio al contexto
        context = super().get_context_data(**kwargs)
        context['servicio_form'] = ServicioForm()  # Formulario adicional para Servicio
        return context

    def form_valid(self, form):
        # Guardar la Solicitud
        solicitud = form.save(commit=False)
        user_cliente = self.request.user.cliente  # Obtener cliente asociado al usuario
        if not user_cliente:
            return redirect('/error_cliente_no_asociado/')  # Redirigir si no hay cliente asociado
        solicitud.cliente = user_cliente  # Asignar el cliente
        solicitud.save()

        # Guardar el Servicio asociado a la Solicitud
        servicio_form = ServicioForm(self.request.POST)
        if servicio_form.is_valid():
            servicio = servicio_form.save(commit=False)
            servicio.solicitud = solicitud  # Asociar el servicio con la solicitud
            servicio.save()

        return super().form_valid(form)
    

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
class HomeView(TemplateView):
    template_name = "base.html"
