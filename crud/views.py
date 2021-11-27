from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from .models import Usuario, Comentario
from .serializers import UsuarioSerializer, ComentarioSerializer

# Create your views here.
#Read-Write: Lista de usuarios
class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

#Read-Write-Delete para un usuario
class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

#Read-Write: Lista de comentarios
class ComentarioList(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

#Read-Write-Delete para un comentario
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class UsuarioComentarios(APIView):
    def get(self, request, author):
        comentarios = Comentario.objects.filter(author=author).order_by('-date')
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data)