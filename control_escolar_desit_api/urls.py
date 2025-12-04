from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import time
from .views.bootstrap import VersionView
from control_escolar_desit_api.views import users
from control_escolar_desit_api.views import alumnos
from control_escolar_desit_api.views import maestros
from control_escolar_desit_api.views import auth
from control_escolar_desit_api.views import bootstrap
from control_escolar_desit_api.views import materias

# Health Check Function
def health_check(request):
    """Endpoint para verificar que la API está funcionando (Render lo usa)"""
    return JsonResponse({
        "status": "healthy",
        "service": "Control Escolar API",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production"
    })

urlpatterns = [
    # Health Check (para Render y monitoreo)
    path('api/health/', health_check, name='health-check'),
    
    # Admin Panel Django
    path('admin-django/', admin.site.urls),
    
    # Create Admin
    path('admin/', users.AdminView.as_view()),
    
    # Admin Data
    path('lista-admins/', users.AdminAll.as_view()),
    
    # Edit Admin (comentado por ahora)
    # path('admins-edit/', users.AdminsViewEdit.as_view()),
    
    # Create Alumno
    path('alumnos/', alumnos.AlumnosView.as_view()),
    
    # Create Maestro
    path('maestros/', maestros.MaestrosView.as_view()),
    
    # Maestro Data
    path('lista-maestros/', maestros.MaestrosAll.as_view()),
    
    # Alumno Data
    path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    
    # Total Users
    path('total-usuarios/', users.TotalUsers.as_view()),
    
    # Materia
    path('materia/', materias.MateriasView.as_view()), 
    
    # Lista de todas las materias
    path('lista-materias/', materias.MateriasAll.as_view()),
    
    # Login
    path('login/', auth.CustomAuthToken.as_view()),
    
    # Logout
    path('logout/', auth.Logout.as_view()),
]

# Solo servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)