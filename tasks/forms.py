#from django.forms import ModelForm
#importamos esta clase para poder acceder a form 
from django import forms
# Importamos el modelo con el cual se creara el formulario
from .models import Task

# class TaskForm(ModelForm):
class TaskForm(forms.ModelForm):
    class Meta:
        # indicamos que modelo es el que tomará como referencia para crear el formularios
        model = Task
        # creamos una lista con los campos que deseamos agregar formulario
        fields = ['title','description','important']
        widgets = {
            # class es atributo de html : from-control es la clase de bootstrap que quiero aplicar
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input'})
        }