from django.db import models

# Create your models here.
class Usuario(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=50)

    def get_comments(self):
       return Comentario.objects.filter( {'autor': self.id} )

class Comentario(models.Model):
    author = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    coment = models.CharField(max_length=200)
    date = models.DateField()