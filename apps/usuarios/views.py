from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, CreateView
from apps.servicios.models import Servicio
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud
from apps.usuarios.forms import ProfesionalForm, SolicitudForm
from apps.servicios.forms import ServicioForm
from apps.usuarios.forms import UsuarioForm, ClienteForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy




# inicio cliente
class DashboardView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        if self.request.user.rol == 'Cliente':
            self.template_name = 'dashboard_cliente.html'
        elif self.request.user.rol == 'Profesional':
            self.template_name = 'dashboard_profesional.html'
        else:
            return False
        return True
    
class AltaUserView(CreateView):
    template_name = 'alta_cliente.html'
    form_class = UsuarioForm

    def get_context_data(self, **kwargs):
        # Añadir los formularios al contexto
        context = super().get_context_data(**kwargs)
        context['cliente_form'] = ClienteForm()  # Formulario de Cliente
        context['profesional_form'] = ProfesionalForm()  # Formulario de Profesional
        return context

    def form_valid(self, form):
        # Guardar el usuario
        usuario = form.save()

        # Validar si es cliente o profesional
        if usuario.rol == 'cliente':  # Asegúrate de que 'rol' sea un campo válido en el modelo Usuario
            cliente_form = ClienteForm(self.request.POST)
            if cliente_form.is_valid():
                cliente = cliente_form.save(commit=False)
                cliente.usuario = usuario
                cliente.save()
            success_url = '/dashboard_cliente/'
        elif usuario.rol == 'profesional':
            profesional_form = ProfesionalForm(self.request.POST)
            if profesional_form.is_valid():
                profesional = profesional_form.save(commit=False)
                profesional.usuario = usuario
                profesional.save()
            success_url = '/dashboard_profesional/'
        else:
            # Si el rol no está definido, redirigir a una página de error o predeterminada
            success_url = '/'

        # Iniciar sesión con el usuario creado
        login(self.request, usuario)
        
        return redirect(success_url)

    
########## ABM SOLICITUDES ############
class CrearSolicitudView(CreateView):
    template_name = 'crear_solicitud.html'
    form_class = SolicitudForm

    def form_valid(self, form):
        # Crear la Solicitud asociada al usuario autenticado
        solicitud = form.save(commit=False)
        solicitud.usuario = self.request.user  # Asocia la solicitud al usuario logueado
        solicitud.save()

        # Verifica si el cliente ya existe o se crea uno nuevo
        cliente, created = Cliente.objects.get_or_create(usuario=self.request.user)
        solicitud.cliente = cliente
        solicitud.save()

        # Redirige a la página deseada
        return redirect('/')


##### ALta Solicitud ######
class CrearSolicitudView(CreateView):
    template_name = 'crear_solicitud.html'
    form_class = SolicitudForm
    success_url = reverse_lazy('crear_solicitud')  # Cambia 'inicio' por la URL adecuada

    def get_form_kwargs(self):
        """
        Pasar el usuario autenticado al formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        solicitud = form.save(commit=False)
        solicitud.cliente = self.request.user.cliente

        # Crear siempre un nuevo Servicio para cada solicitud
        servicio = Servicio.objects.create(
            nombre_servicio=form.cleaned_data['nombre_servicio'],
            descripcion=form.cleaned_data['descripcion_servicio']
        )
        solicitud.servicio = servicio
        solicitud.save()
        return redirect(self.success_url)
    
########## ABM SOLICITUDES ############










class HomeView(TemplateView):
    template_name = "base.html"
