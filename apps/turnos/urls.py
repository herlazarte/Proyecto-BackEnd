from django.urls import path
from .views import AsignarTurnoView

urlpatterns = [
path('solicitud/asignar-turno/<int:solicitud_id>/', AsignarTurnoView.as_view(), name='asignar_turno'),
]