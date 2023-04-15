from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# Create your views here.


def home(request):

    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    elif request.method == 'POST':
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                # metodo para cifrar y preparar los datos para ser guardados en la tabla
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # guardar en la tabla de BD
                login(request, user)  # crea una session en la cookies
                return redirect('tasks')
                # return HttpResponse('User created successfully')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Error: Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Error: Password do not match'
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks,
    })

@login_required    
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks,
    })    

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    elif request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            #print(form)#muestra la estructura html de un form
            new_task = form.save(commit=False)#guarda el form enviado por el metodo POST
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')            
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valid data'
            })            

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        
        form = TaskForm(instance=task)
        
        return render(request, 'task_detail.html', {
        'task': task,
        'form': form
        })
    elif request.method == 'POST':
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            
            form = TaskForm(request.POST, instance=task)
            
            form.save()
            
            return redirect('tasks')            
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'Error updating task'
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')    

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':#enviar datos hacia el FrontEnd
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    elif request.method == 'POST':#enviar datos hacia el BackEnd
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            # valida que el user este autenticado y si es correcto redirecciona a la carpeta task "return redirect('tasks')"
            login(request, user)
            return redirect('tasks')
        # return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
