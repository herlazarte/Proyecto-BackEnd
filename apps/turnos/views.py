from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from apps.turnos.models import Turno
from apps.solicitudes.models import Solicitud
from apps.turnos.forms import TurnoForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class AsignarTurnoView(FormView):
    template_name = 'asignar_turno.html'
    form_class = TurnoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud_id = self.kwargs['solicitud_id']
        solicitud = get_object_or_404(Solicitud, id=solicitud_id)
        context['solicitud'] = solicitud
        return context

    def form_valid(self, form):
        solicitud = get_object_or_404(Solicitud, id=self.kwargs['solicitud_id'])

        # Verificar si el usuario tiene el rol de "Profesional"
        if self.request.user.rol != 'Profesional':
            # Mostrar un mensaje de error y redirigir
            messages.error(self.request, "No tienes permiso para asignar turnos.")
            # return redirect('home')  # Redirigir a la página principal, por ejemplo

        # Verificar si el usuario tiene un 'profesional' asociado
        if not hasattr(self.request.user, 'profesional'):
            # Mostrar un mensaje de error y redirigir
            messages.error(self.request, "Tu cuenta no tiene un profesional asociado.")
            # return redirect('home')  # O redirigir a otra página que tenga sentido

        turno = form.save(commit=False)
        turno.solicitud = solicitud
        turno.profesional = self.request.user.profesional  # Asociamos el turno al profesional logueado
        turno.cliente = solicitud.cliente  # Asociamos el turno al cliente que hizo la solicitud
        turno.save()

        # Redirigir al detalle del turno
        messages.success(self.request, "Turno asignado correctamente.")
        return redirect('asignar_turno')

    def form_invalid(self, form):
        solicitud = get_object_or_404(Solicitud, id=self.kwargs['solicitud_id'])
        return self.render_to_response(self.get_context_data(form=form, solicitud=solicitud))