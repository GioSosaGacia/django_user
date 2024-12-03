from django.contrib import admin
from .models import Task

# esta clase nos permite ver en la interfaz de admin campos de solo lectura como el campo created ya que es un campo que se llena de manera automatica al crear cualquier tarea
# Hereda todo lo que este en admin.ModelAdmin
class TaskAdmin(admin.ModelAdmin):
    # Indicamos que son campos de solo lectura, colocamos una coma al final porque es una tupla
    readonly_fields = ("created", )
    
# Register your models here.
admin.site.register(Task, TaskAdmin)