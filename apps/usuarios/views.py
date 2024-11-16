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
    template_name = 'alta_cliente.html'
    form_class = UsuarioForm
    success_url = '/dashboard_cliente/'  # Redirección por defecto (para clientes)

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

        # Redirigir según el rol del Usuario
        if usuario.rol == 'Profesional':  # Si el Usuario es profesional
            return redirect('/dashboard_profesional/')  # Redirección para profesionales
        else:
            return redirect('/dashboard_cliente/')  # Redirección para clientes


########## ABM SOLICITUDES ############
class HomeView(TemplateView):
    template_name = "base.html"
