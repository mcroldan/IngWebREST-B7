from django.urls import path
from crud import views

urlpatterns = [
    path('usuario/', views.UsuarioList.as_view()),
    path('usuario/<int:pk>', views.UsuarioDetail.as_view()),
    path('usuario/<str:name>', views.UsuarioPorNombre.as_view()),
    path('usuario/<int:author>/comentario', views.UsuarioComentarios.as_view()),
    path('comentario/', views.ComentarioList.as_view()),
    path('comentario/<int:pk>/', views.ComentarioDetail.as_view()),
    path('comentario/<slug:date>/', views.ComentariosFecha.as_view())
    
]