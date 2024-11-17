from django.urls import path
from .views import HomeView,AltaUserView, DashboardView, CrearSolicitudView, ActualizarSolicitudView, EliminarSolicitudView, ListarSolicitudesView  # Importa las vistas de la aplicación

urlpatterns = [
    # Ruta para registrar usuarios, se agregará una vista específica en `views.py`
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('AltaUser/', AltaUserView.as_view(), name='AltaUser'),
    path('crear_solicitud/', CrearSolicitudView.as_view(), name='crear_solicitud'),
     path('actualizar_solicitud/<int:pk>/', ActualizarSolicitudView.as_view(), name='actualizar_solicitud'),
    path('eliminar_solicitud/<int:pk>/', EliminarSolicitudView.as_view(), name='eliminar_solicitud'),
    path('listar_solicitudes/', ListarSolicitudesView.as_view(), name='listar_solicitudes'),

    
    path('', HomeView.as_view(), name='home'),

]