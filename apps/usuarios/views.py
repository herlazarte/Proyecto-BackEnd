from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
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


class AltaUserView(CreateView):
    template_name = 'alta_user.html'
    form_class = UsuarioForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_form'] = ClienteForm()
        context['profesional_form'] = ProfesionalForm()
        return context

    def form_valid(self, form):
        # Guardamos el usuario
        usuario = form.save()

        # Si es cliente, guardamos los datos del cliente
        if usuario.rol == 'cliente':
            cliente_form = ClienteForm(self.request.POST)
            if cliente_form.is_valid():
                cliente = cliente_form.save(commit=False)
                cliente.usuario = usuario
                cliente.save()
            success_url = '/dashboard_cliente/'

        # Si es profesional, guardamos los datos del profesional
        elif usuario.rol == 'profesional':
            profesional_form = ProfesionalForm(self.request.POST)
            if profesional_form.is_valid():
                profesional = profesional_form.save(commit=False)
                profesional.usuario = usuario
                profesional.save()
            success_url = '/dashboard_profesional/'

        # Iniciar sesión y redirigir
        login(self.request, usuario)
        return redirect(success_url)
    

# inicio
class DashboardView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        if self.request.user.rol == 'Cliente':
            self.template_name = 'dashboard_cliente.html'
        elif self.request.user.rol == 'Profesional':
            self.template_name = 'dashboard_profesional.html'
        else:
            return False
        return True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.rol == 'Cliente':
            # Agregar las solicitudes del cliente autenticado al contexto
            context['solicitudes'] = Solicitud.objects.filter(cliente=self.request.user.cliente)
        return context


    
########## ABM SOLICITUDES ############

# class ListarSolicitudesView(ListView):
#     template_name = 'listar_solicitudes.html'
#     model = Solicitud
#     context_object_name = 'solicitudes'

#     def get_queryset(self):
#         """
#         Filtrar las solicitudes del cliente autenticado.
#         """
#         return Solicitud.objects.filter(cliente=self.request.user.cliente)


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
    

class ActualizarSolicitudView(UpdateView):
    template_name = 'actualizar_solicitud.html'
    model = Solicitud
    form_class = SolicitudForm
    success_url = reverse_lazy('dashboard_cliente')  # Redirige a la lista de solicitudes

    def get_form_kwargs(self):
        """
        Pasar el usuario autenticado al formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        solicitud = form.save(commit=False)
        solicitud.cliente = self.request.user.cliente  # Asegurar que el cliente no cambie
        solicitud.save()
        return redirect(self.success_url)

class EliminarSolicitudView(DeleteView):
    template_name = 'eliminar_solicitud.html'
    model = Solicitud
    success_url = reverse_lazy('dashboard_cliente')  # Redirige a la lista de solicitudes

    def get_queryset(self):
        """
        Limitar las solicitudes que puede eliminar al cliente autenticado.
        """
        return Solicitud.objects.filter(cliente=self.request.user.cliente)

    
########## ABM SOLICITUDES ############










class HomeView(TemplateView):
    template_name = "base.html"
