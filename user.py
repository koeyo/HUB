from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.username
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registrar.html', {'form': form})
