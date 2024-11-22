from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import TaskForm 
from .models import Task
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
    #CONSULTA
    #trae todos los Objetos
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'tasks.html', {'tasks':tasks})

def create_task(request):
    if request.method == 'GET':
        
        return render(request, 'create_task.html',{
            'form':TaskForm
        })
    else:
        try:
            #print(request.POST)
            form = TaskForm(request.POST)
            #print(form)
            #guardar datos
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
            'form':TaskForm,
            'error':'INGRESA datos VALIDOS'
            })

def task_detail(request,task_id):
    #Busca por id
    #task = Task.objects.get(pk=task_id)
    task = get_object_or_404(Task, pk=task_id)
    #print(task_id)
    return render(request,'task_detail.html',{'task':task})

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
        
        