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
from django.contrib.auth.hashers import make_password



class AltaUserView(CreateView):
    template_name = 'alta_user.html'
    form_class = UsuarioForm

    
    def get(self, request, *args, **kwargs):
        usuario_form = UsuarioForm()
        cliente_form = ClienteForm()
        profesional_form = ProfesionalForm()
        return self.render_to_response({
            'usuario_form': usuario_form,
            'cliente_form': cliente_form,
            'profesional_form': profesional_form,
            'mostrar_cliente': False,
            'mostrar_profesional': False,
        })

    def post(self, request, *args, **kwargs):
        usuario_form = UsuarioForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        profesional_form = ProfesionalForm(request.POST)

        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            rol = usuario_form.cleaned_data['rol']

            if rol == 'Cliente' and cliente_form.is_valid():
                usuario.save()
                cliente = cliente_form.save(commit=False)
                cliente.usuario = usuario
                cliente.save()
                #return redirect('dashboard')  # Redirige tras el éxito
            elif rol == 'Profesional' and profesional_form.is_valid():
                usuario.save()
                profesional = profesional_form.save(commit=False)
                profesional.usuario = usuario
                profesional.save()
                #return redirect('dashboard')  # Redirige tras el éxito

        # Si hay errores, muestra los formularios con validación fallida
        return self.render_to_response({
            'usuario_form': usuario_form,
            'cliente_form': cliente_form,
            'profesional_form': profesional_form,
            'mostrar_cliente': usuario_form.cleaned_data.get('rol') == 'Cliente',
            'mostrar_profesional': usuario_form.cleaned_data.get('rol') == 'Profesional',
        })

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
    success_url = reverse_lazy('dashboard')  # Cambia 'inicio' por la URL adecuada

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
    success_url = reverse_lazy('dashboard')  # Redirige a la lista de solicitudes

    def get_form_kwargs(self):
        """
        Pasar el usuario autenticado al formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

    def form_valid(self, form):
        solicitud = form.save(commit=False)

        # Actualizar el Servicio
        servicio = solicitud.servicio
        servicio.nombre_servicio = form.cleaned_data['nombre_servicio']
        servicio.descripcion = form.cleaned_data['descripcion_servicio']
        servicio.save()

        return super().form_valid(form)
  
  



class EliminarSolicitudView(DeleteView):
    template_name = 'eliminar_solicitud.html'
    model = Solicitud
    success_url = reverse_lazy('dashboard')  # Redirige a la lista de solicitudes

    def get_queryset(self):
        """
        Limitar las solicitudes que puede eliminar al cliente autenticado.
        """
        return Solicitud.objects.filter(cliente=self.request.user.cliente)

    
########## ABM SOLICITUDES ############










class HomeView(TemplateView):
    template_name = "base.html"
