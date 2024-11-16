from django.urls import path
from .views import HomeView,AltaUserView, DashboardView, CrearSolicitudView  # Importa las vistas de la aplicación

urlpatterns = [
    # Ruta para registrar usuarios, se agregará una vista específica en `views.py`
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('AltaUser/', AltaUserView.as_view(), name='AltaUser'),
    path('crear_solicitud/', CrearSolicitudView.as_view(), name='crear_solicitud'),
    
    path('', HomeView.as_view(), name='home'),

]