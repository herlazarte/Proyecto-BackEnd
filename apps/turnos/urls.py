from django.urls import path
from .views import AsignarTurnoView

urlpatterns = [
path('solicitud/<int:solicitud_id>/asignar-turno/', AsignarTurnoView.as_view(), name='asignar_turno'),
]