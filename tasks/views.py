#recibe respuestas http
from django.http import HttpResponse
# Permite renderizar los templates html 
from django.shortcuts import render

# django por defecto ya contiene un formularario para la autenticaion de usarios y para utilizarlo debemos de importar la siguiente clase ->UserCreationForm
from django.contrib.auth.forms import UserCreationForm
# Para crear usuarios importa la clase User
from django.contrib.auth.models import User


# Create your views here.


#view to create the form and create users
def home(request):
    return render(request, 'home.html')
def singup(request):
    if request.method == 'GET':
        print('Enviando formulario')
        return render(request, 'singup.html',{
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user 
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse('User created successfuly')
            except:
                return HttpResponse('User already exists')
        return HttpResponse('Password do not match')
        
    