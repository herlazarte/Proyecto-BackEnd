from django.urls import path
from . import views

urlpatterns = [
    path('listado_solicitudes/', views.SolicitudesView.as_view(), name='listado_solicitudes'),
    path('listado_solicitudes_cliente/', views.SolicitudesClienteView.as_view(), name='listado_solicitudes_cliente'),
]