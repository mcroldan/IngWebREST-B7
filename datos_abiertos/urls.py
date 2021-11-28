
from django.urls import path 
import datos_abiertos.views

urlpatterns = [
    path('aparcamientos', datos_abiertos.views.get_aparcamientos),
    path('aparcamientos/radio/<str:lon>/<str:lat>/<int:radius>', datos_abiertos.views.get_aparcamientos_dentro),
    path('aparcamientos/cerca/<str:lon>/<str:lat>', datos_abiertos.views.get_aparcamiento_cercano),
    path('atascos', datos_abiertos.views.get_atascos),
    path('atascos/cerca/<str:lon>/<str:lat>', datos_abiertos.views.get_atasco_cercano),
    path('atascos/radio/<str:lon>/<str:lat>/<int:radius>', datos_abiertos.views.get_atascos_dentro),

    path('json_aparcamientos', datos_abiertos.views.get_json_aparcamientos),
    path('json_aparcamientos/radio/<str:lon>/<str:lat>/<int:radius>', datos_abiertos.views.get_json_aparcamientos_dentro),
    path('json_aparcamientos/cerca/<str:lon>/<str:lat>', datos_abiertos.views.get_json_aparcamiento_cercano),
    path('json_atascos', datos_abiertos.views.get_json_atascos),
    path('json_atascos/cerca/<str:lon>/<str:lat>', datos_abiertos.views.get_json_atasco_cercano),
    path('json_atascos/radio/<str:lon>/<str:lat>/<int:radius>', datos_abiertos.views.get_json_atascos_dentro),
]
