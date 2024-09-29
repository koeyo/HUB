from django.urls import path
from .views import registrar_usuario

urlpatterns = [
    path('registrar/', registrar_usuario, name='registrar_usuario'),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('', include('projetos.urls')),
]
from django.urls import path
from .views import feed, dashboard, adicionar_projeto, editar_projeto, deletar_projeto

urlpatterns = [
    path('', feed, name='feed'),
    path('dashboard/', dashboard, name='dashboard'),
    path('adicionar/', adicionar_projeto, name='adicionar_projeto'),
    path('editar/<int:projeto_id>/', editar_projeto, name='editar_projeto'),
    path('deletar/<int:projeto_id>/', deletar_projeto, name='deletar_projeto'),
]
