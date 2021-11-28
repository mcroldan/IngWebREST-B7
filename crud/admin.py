from django.contrib import admin
from .models import Comentario, Usuario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Comentario)