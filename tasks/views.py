# recibe respuestas http
from django.http import HttpResponse
# Permite renderizar los templates html
from django.shortcuts import render, redirect, get_object_or_404

# django por defecto ya contiene un formularario para la autenticaion de usarios y para utilizarlo debemos de importar la siguiente clase ->UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Para crear usuarios importa la clase User
from django.contrib.auth.models import User
# permite crear una cookie que indica que se ha iniciado sesión, nota: no valida que los datos sean correctos, logout permite cerrar sesión
from django.contrib.auth import login, logout, authenticate
# tambien podemos usar errores especificos como integrity error
from django.db import IntegrityError
#importamos el formulario creado en forms.py
from .forms import TaskForm
from .models import Task
#importamos esta clase para saber la fecha enla que se finalizo la tarea
from django.utils import timezone
#Una forma de requerir login para entrar a determinadas secciones dentro de un programa, en este caso para crea un atarea es indispenszable estar logeado o iniciar seción  y con login_requiret podemos hacerlo, si no estas logeado te redirige a la pestaña de login y para ello debemos de insertar en settings.py la propiedad LOGIN_URL = 'singin' y con ello nos redireccionara a la ventana de login para iniciar sesión.
from django.contrib.auth.decorators import login_required

# Create your views here.


# view to create the form and create users
def home(request):
    return render(request, 'home.html')


def singup(request):
    if request.method == 'GET':
        print('Enviando formulario')
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # return HttpResponse('User created successfuly')
                # indica que el usuario esta conectado en tasks y lo podemos ver en modo desarrollo apartado aplicación y en cookies, se abre un sessionid
                login(request, user)
                # al agregar un usuario y guardarlo nos redirecciona a tasks, al ejecutar return se finaliza cualquier funcion o seccion de codigo..
                return redirect('tasks')
            except IntegrityError:  # -> podemos considerar exepciones a errores en especifico
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
                # de esta manera en vez de que cargue un template con el error lo redirige al mismo template y en la parte superior agrega el error, mostrando la página del formulario
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


@login_required
def tasks(request):
    # De esta manera me arrojará todas la tareas insertadas dentro de la base de datos
    #Task.objects.all()
    #De estra otra forma me arrojara solo las tareas del usuario que esta logeado.
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html',{'tasks':tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
    # Para guardar los datos dentro de la base de datos:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
            'form': TaskForm,
            'error':'Please provide a valida data'
        })
            

@login_required
def task_detail(request, task_id):
    #Esta line permite obtener las tareas, pero si no encuantra una tarea marcara error
    #task = Task.objects.get(pk=task_id)
    #con get.object_ot_404 si no encuentra una tarea envia el 404 de not found y ya no se vera tan feo con en lalinea anterior
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # Intanciamos task , instance -> recibe un modelo que en este caso es task
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) #user=request.user nos permite que cada usario solo vea las tareas relacionadas al mismo y no las de otros usuarios
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html', {'task':task, 'form':form, 'error':'Error updating task'})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
        
  
@login_required      
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
    

# usa la clase de logout la cual debemos de importar, no se puede usar logout como nombre de la función si no marcará error, al cerrar la sesión nos enviara a home
def singout(request):
    logout(request)
    return redirect('home')


def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        # print(request.POST)
        user =authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect' 
            })
        else:
            login(request, user)
            return redirect('tasks')
        
        

    
