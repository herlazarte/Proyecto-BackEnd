from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from apps.turnos.models import Turno
from apps.solicitudes.models import Solicitud
from apps.turnos.forms import TurnoForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


class AsignarTurnoView(FormView):
    template_name = 'asignar_turno.html'
    form_class = TurnoForm

    def get_context_data(self, **kwargs):
        """Agregamos la solicitud al contexto para usarla en el template."""
        context = super().get_context_data(**kwargs)
        solicitud_id = self.kwargs['solicitud_id']
        solicitud = get_object_or_404(Solicitud, id=solicitud_id)
        context['solicitud'] = solicitud
        return context

    def form_valid(self, form):
        solicitud = get_object_or_404(Solicitud, id=self.kwargs['solicitud_id'])

        # Verificar si el usuario tiene permisos de profesional
        if not hasattr(self.request.user, 'profesional'):
            messages.error(self.request, "Tu cuenta no tiene un profesional asociado o permisos para asignar turnos.")
            return redirect('home')

        # Crear el turno con el estado seleccionado
        turno = form.save(commit=False)
        turno.solicitud = solicitud
        turno.profesional = self.request.user.profesional
        turno.save()

        # Actualizar el estado de la solicitud según la decisión del profesional
        solicitud.estado = turno.estado
        solicitud.save()

        # Mensaje de éxito y redirección
        messages.success(self.request, "Turno asignado correctamente. La solicitud ha sido actualizada.")
        # return redirect('asignar_turno', solicitud_id=solicitud.id)
        return redirect(reverse_lazy('listado_solicitudes'))

    def form_invalid(self, form):
        """Renderiza la página nuevamente con los errores."""
        messages.error(self.request, "Por favor corrige los errores del formulario.")
        return self.render_to_response(self.get_context_data(form=form))