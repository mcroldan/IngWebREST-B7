
from typing import ValuesView
from django.urls import path 
import datos_abiertos.views

urlpatterns = [
    path('get/aparcamientos', datos_abiertos.views.get_aparcamientos),
    path('get/aparcamientos/radio/<str:lon>/<str:lat>/<int:radius>', datos_abiertos.views.get_aparcamientos_dentro),
    path('get/aparcamientos/cerca/<str:lon>/<str:lat>', datos_abiertos.views.get_aparcamiento_cercano),
    path('get/atascos', datos_abiertos.views.get_atascos),
    path('get/atascos/cerca/<str:lon>/<str:lat>', datos_abiertos.views.get_atasco_cercano),
    path('get/atascos/radio/<str:lon>/<str:lat>/<int:radius>', datos_abiertos.views.get_atascos_dentro),
]
