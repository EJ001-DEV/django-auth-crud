from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

#para colocar el modelo task en el ORM del panel de administrador, se importa el modelo y luego se indica en el panel admin: admin.site.register(task)
# Register your models here.
admin.site.register(Task, TaskAdmin)