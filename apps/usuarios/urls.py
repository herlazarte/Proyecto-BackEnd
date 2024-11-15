from django.urls import path
from .views import HomeView,AltaClientesView, DashboardView  # Importa las vistas de la aplicación

urlpatterns = [
    # Ruta para registrar usuarios, se agregará una vista específica en `views.py`
    path('alta_cliente/', AltaClientesView.as_view(), name='alta_cliente'),
    path('dashboard_cliente/', DashboardView.as_view(), name='dashboard_cliente'),
    path('', HomeView.as_view(), name='home'),

]