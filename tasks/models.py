from django.db import models
# iMPORTAMOS LA clase User para hacer la relacion de la tabla Task con User
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True) #blanck=True indica que es opcional solo el admin y no en la base de datos
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #elimina datos en cascada
    
    # esta funcion nos permite ver el titulo de la tarea que de agrego en la interfaz, antes de esta funcion solo mostraba task1
    def __str__(self):
        return self.title + ' -by ' + self.user.username