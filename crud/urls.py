from django.urls import path
from crud import views
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="CRUD API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('usuario/', views.UsuarioList.as_view()),
    path('usuario/<int:pk>/', views.UsuarioDetail.as_view()),
    path('usuario/<str:name>/', views.UsuarioPorNombre.as_view()),
    path('usuario/<int:author>/comentario/', views.UsuarioComentarios.as_view()),
    path('comentario/', views.ComentarioList.as_view()),
    path('comentario/<int:pk>/', views.ComentarioDetail.as_view()),
    path('comentario/<slug:date>/', views.ComentariosFecha.as_view()),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]