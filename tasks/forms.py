from django.forms import ModelForm
# Importamos el modelo con el cual se creara el formulario
from .models import Task

class TaskForm(ModelForm):
    class Meta():
        # indicamos que modelo es el que tomará como referencia para crear el formularios
        model = Task
        # creamos una lista con los campos que deseamos agregar formulario
        fields = ['title','description','important']