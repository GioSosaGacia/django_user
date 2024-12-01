from django.http import HttpResponse
from django.shortcuts import render

# django por defecto ya contiene un formularario para la autenticaion de usarios y para utilizarlo debemos de importar la siguiente clase ->UserCreationForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def helloword(request):
    title = 'Hello world'
    return render(request, 'singup.html',{
        'form' : UserCreationForm #-> crea un formulario creado en usercreationform y se renderiza a singup.html
    })