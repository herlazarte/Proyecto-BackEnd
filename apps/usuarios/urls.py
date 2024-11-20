from django.urls import path
from .views import HomeView,UsuarioCreateView, DashboardView, CrearSolicitudView, ActualizarSolicitudView, EliminarSolicitudView # Importa las vistas de la aplicación

urlpatterns = [
    # Ruta para registrar usuarios, se agregará una vista específica en `views.py`
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  
    path('AltaUser/', UsuarioCreateView.as_view(), name='AltaUser'),
    #path('profesional_create/', ProfesionalCreateView.as_view(), name='profesional_create'),
    path('crear_solicitud/', CrearSolicitudView.as_view(), name='crear_solicitud'),
    path('actualizar_solicitud/<int:id>/', ActualizarSolicitudView.as_view(), name='actualizar_solicitud'),
    path('eliminar_solicitud/<int:id>/', EliminarSolicitudView.as_view(), name='eliminar_solicitud'),
   
    path('', HomeView.as_view(), name='home'),

]