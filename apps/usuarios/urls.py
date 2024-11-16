from django.urls import path
from .views import HomeView,AltaUserView, DashboardView, CrearSolicitudView, DashboardProfesionalView  # Importa las vistas de la aplicación

urlpatterns = [
    # Ruta para registrar usuarios, se agregará una vista específica en `views.py`
    path('dashboard_cliente/', DashboardView.as_view(), name='dashboard_cliente'),
    path('dashboard_profesional/', DashboardProfesionalView.as_view(), name='dashboard_profesional'),
    path('AltaUser/', AltaUserView.as_view(), name='AltaUser'),
    path('crear_solicitud/', CrearSolicitudView.as_view(), name='crear_solicitud'),
    
    path('', HomeView.as_view(), name='home'),

]