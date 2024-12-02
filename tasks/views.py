# recibe respuestas http
from django.http import HttpResponse
# Permite renderizar los templates html
from django.shortcuts import render, redirect

# django por defecto ya contiene un formularario para la autenticaion de usarios y para utilizarlo debemos de importar la siguiente clase ->UserCreationForm
from django.contrib.auth.forms import UserCreationForm
# Para crear usuarios importa la clase User
from django.contrib.auth.models import User
#permite crear una cookie que indica que se ha iniciado sesión, nota: no valida que los datos sean correctos
from django.contrib.auth import login
#tambien podemos usar errores especificos como integrity error
from django.db import IntegrityError


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
                #return HttpResponse('User created successfuly')
                #indica que el usuario esta conectado en tasks y lo podemos ver en modo desarrollo apartado aplicación y en cookies, se abre un sessionid
                login(request, user)
                #al agregar un usuario y guardarlo nos redirecciona a tasks, al ejecutar return se finaliza cualquier funcion o seccion de codigo.. 
                return redirect('tasks')
            except IntegrityError: #-> podemos considerar exepciones a errores en especifico
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
                # de esta manera en vez de que cargue un template con el error lo redirige al mismo template y en la parte superior agrega el error, mostrando la página del formulario
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })
        
        
def tasks(request):
    return render(request,'tasks.html')