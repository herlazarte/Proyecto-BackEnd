from pyexpat.errors import messages
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from apps.servicios.models import Servicio
from apps.usuarios.models import Cliente, Usuario
from apps.solicitudes.models import Solicitud
from apps.usuarios.forms import ProfesionalForm, SolicitudForm
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.views.generic.edit import FormView




from apps.usuarios.forms import UsuarioForm, ClienteForm

from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404



class UsuarioCreateView(CreateView):
    model = Cliente
    fields = ['direccion', 'telefono']
    template_name = 'crear_usuario.html'
    success_url = '/clientes/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_form'] = UsuarioForm()  # Formulario para crear Usuario
        context['cliente_form'] = ClienteForm()  # Formulario para crear Cliente
        context['profesional_form'] = ProfesionalForm()  # Formulario para crear Profesional
        return context

    def post(self, request, *args, **kwargs):
        usuario_form = UsuarioForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        profesional_form = ProfesionalForm(request.POST)

        # Si el formulario de Usuario es válido
        if usuario_form.is_valid():
            # Guardar el usuario sin el commit para poder manipular la contraseña
            usuario = usuario_form.save(commit=False)
            usuario.set_password(usuario_form.cleaned_data['password'])
            usuario.save()  # Guardar el Usuario

            # Verificar el rol del usuario desde el objeto usuario
            if usuario.rol == 'Cliente':
                if cliente_form.is_valid():
                    cliente = cliente_form.save(commit=False)
                    cliente.usuario = usuario  # Asignar el usuario al perfil de Cliente
                    cliente.save()  # Guardar el perfil de Cliente
            elif usuario.rol == 'Profesional':
                if profesional_form.is_valid():
                    profesional = profesional_form.save(commit=False)
                    profesional.usuario = usuario  # Asignar el usuario al perfil de Profesional
                    profesional.save()  # Guardar el perfil de Profesional

            return redirect(reverse_lazy('home'))
        # Si no es válido, renderizar nuevamente con los errores
        return render(request, self.template_name, {
            'usuario_form': usuario_form,
            'cliente_form': cliente_form,
            'profesional_form': profesional_form,
        })

# inicio
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol is not None

    def get_template_names(self):
        if self.request.user.rol == 'Cliente':
            return ['dashboard_cliente.html']
        elif self.request.user.rol == 'Profesional':
            return ['dashboard_profesional.html']
        else:
            return ['base.html']  # Plantilla por defecto
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
    success_url = reverse_lazy('dashboard')  # Cambia 'dashboard' por la URL adecuada

    def get_form_kwargs(self):
        """
        Pasar el usuario autenticado al formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Verificamos que el usuario tenga un cliente asociado
        if not hasattr(self.request.user, 'cliente'):
            # Si no tiene un cliente asociado, redirige a una vista de error
            return redirect('error_no_cliente')  # Redirige a una vista de error o muestra un mensaje

        # Si el usuario tiene un cliente, procedemos
        cliente = self.request.user.cliente
        solicitud = form.save(commit=False)
        solicitud.cliente = cliente

        # Crear o obtener un servicio existente
        servicio, created = Servicio.objects.get_or_create(
            nombre_servicio=form.cleaned_data['nombre_servicio'],
            descripcion=form.cleaned_data['descripcion_servicio']
        )
        solicitud.servicio = servicio
        solicitud.save()

        return redirect(self.success_url)



class ActualizarSolicitudView(UpdateView):
    model = Solicitud
    template_name = 'actualizar_solicitud.html'
    form_class = SolicitudForm
    success_url = reverse_lazy('listado_solicitudes_cliente')

    def get_object(self, queryset=None):
        return get_object_or_404(Solicitud, id=self.kwargs['id'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        servicio = self.get_object().servicio
        if servicio:
            initial['nombre_servicio'] = servicio.nombre_servicio
            initial['descripcion_servicio'] = servicio.descripcion
        return initial

    def form_valid(self, form):
        solicitud = form.save(commit=False)
        servicio = solicitud.servicio
        if servicio:
            servicio.nombre_servicio = form.cleaned_data['nombre_servicio']
            servicio.descripcion = form.cleaned_data['descripcion_servicio']
            servicio.save()
        return super().form_valid(form)


class EliminarSolicitudView(TemplateView):
    template_name = 'eliminar_solicitud.html'

    def get(self, request, *args, **kwargs):
        # Obtener la solicitud a eliminar
        solicitud = get_object_or_404(Solicitud, id=kwargs['id'])
        return self.render_to_response({'solicitud': solicitud})

    def post(self, request, *args, **kwargs):
        # Obtener la solicitud a eliminar
        solicitud = get_object_or_404(Solicitud, id=kwargs['id'])
        solicitud.delete()  # Eliminar la solicitud
        return redirect('listado_solicitudes_cliente') 
    
########## ABM SOLICITUDES ############










class HomeView(TemplateView):
    template_name = "base.html"
