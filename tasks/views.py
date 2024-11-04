from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
#Respuesta HTTP
#from django.http import HttpResponse
# Create your views here.

def home(request):
    #title = 'Creando Formulario'
    return render(request,'home.html')


def signup(request):
    #title = 'Creando Formulario'
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form':UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Registrar Usuario
                user = User.objects.create_user(
                    username= request.POST['username'],
                    password= request.POST['password1'])
                user.save()
                #Guardar cookis de inicio de sesion
                login(request, user)
                #redireccionar
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{
                    'form':UserCreationForm,
                    'error':'El usuario Ya existe'
                })
        return render(request,'signup.html',{
            'form':UserCreationForm,
            'error':'Contraseña No existe'
        })

def tasks(request):
    return render(request,'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
            'form':AuthenticationForm
        })
    else:
        #valida si el usuario esta autenticado usando authenticate
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        #valida 
        if user is None:
            return render(request,'signin.html',{
            'form':AuthenticationForm,
            'error':'Username or password is incorrect'
            })
        else:
            #Guardar cookis de inicio de sesion
            login(request, user)
            return redirect('tasks')
        
        