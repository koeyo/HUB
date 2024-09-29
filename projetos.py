from django.db import models
from usuarios.models import Usuario

class Projeto(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='projetos')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
INSTALLED_APPS = [
    # Outros apps padrões do Django
    'usuarios',
    'projetos',
]
from django.shortcuts import render
from .models import Projeto

def feed(request):
    projetos = Projeto.objects.all().order_by('-data_criacao')
    return render(request, 'projetos/feed.html', {'projetos': projetos})
from django.urls import path
from .views import feed

urlpatterns = [
    path('', feed, name='feed'),
]
from django.shortcuts import render
from .models import Projeto
from django.db.models import Q

def feed(request):
    query = request.GET.get('q')  # Captura o parâmetro da query de busca
    if query:
        projetos = Projeto.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        ).order_by('-data_criacao')
    else:
        projetos = Projeto.objects.all().order_by('-data_criacao')

    return render(request, 'projetos/feed.html', {'projetos': projetos, 'query': query})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Projeto
from .forms import ProjetoForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    projetos = Projeto.objects.filter(autor=request.user)
    return render(request, 'projetos/dashboard.html', {'projetos': projetos})

@login_required
def adicionar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.autor = request.user
            projeto.save()
            return redirect('dashboard')
    else:
        form = ProjetoForm()
    return render(request, 'projetos/adicionar_projeto.html', {'form': form})

@login_required
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, autor=request.user)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjetoForm(instance=projeto)
    return render(request, 'projetos/editar_projeto.html', {'form': form})

@login_required
def deletar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, autor=request.user)
    if request.method == 'POST':
        projeto.delete()
        return redirect('dashboard')
    return render(request, 'projetos/deletar_projeto.html', {'projeto': projeto})
from django import forms
from .models import Projeto

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao']
