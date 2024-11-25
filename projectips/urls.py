"""
URL configuration for projectips project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appips.views import *

urlpatterns = [   
    path('admin/', admin.site.urls),
    path('crear_usuario/', UsuarioCreate.as_view(), name='crear_usuario'),
    path('crear_medico/', MedicoCreate.as_view(), name='crear_medico'),
    path('home/',home, name='home'), 
    path('listar/',listar_usuarios, name='listar_usuarios'),
    path('listar_medicos/',listar_medicos, name='listar_medicos'),
    path('usuarios/editar/<str:pk>/', UsuarioUpdate.as_view(), name='editar_usuario'),
    path('medicos/editar/<str:pk>/', MedicoUpdate.as_view(), name='editar_medico'),
    path('usuarios/eliminar/<str:pk>/', UsuarioDelete.as_view(), name='eliminar_usuario'),
    path('medicos/eliminar/<str:pk>/', MedicoDelete.as_view(), name='eliminar_medico'),
    path('lista_citas/', CitasLista.as_view(), name='lista_citas'),
    path('crear_cita/',CitaCreate.as_view(), name='crear_citas'),
    path('editar_cita/<str:pk>/', CitaUpdate.as_view(), name='editar_cita'),
    path('cita_eliminar/<str:pk>/', CitaDelete.as_view(), name='eliminar_cita'),
    path('historias-clinicas/', HistoriaClinicaListView.as_view(), name='listar_historias_clinicas'),
    path('historias-clinicas/<int:pk>/', HistoriaClinicaDetailView.as_view(), name='detalle_historia_clinica'),
    #path('historias-clinicas/<int:historia_clinica_id>/registros-citas/', RegistroCitaListView.as_view(), name='listar_registros_citas_por_historia'),
    path('citas/<int:pk>/completar/', CompletarCitaView.as_view(), name='completar_cita'),
    path('historias-clinicas/<int:historia_clinica_id>/registros-citas/', RegistroCitaListView.as_view(), name='listar_registros_citas'),
    
]