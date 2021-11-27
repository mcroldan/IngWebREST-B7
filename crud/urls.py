
from typing import ValuesView
from django.urls import path 
import crud.views

urlpatterns = [
    path('get/users', crud.views.get_all_users),#
    path('get/comments', crud.views.get_all_comments),#
    path('get/users/<str:var>', crud.views.get_user),#
    path('get/comments/<str:var>', crud.views.get_comment),  #
    path('get/usercomments/<str:var>', crud.views.get_user_comments),#
    path('post/users/<str:name>/<str:surname>/<str:address>', crud.views.create_user),
    path('post/comments/<str:autor>/<str:comentario>/<str:fecha>', crud.views.create_comment),  
    path('put/users/<str:id>/<str:attr>/<str:newAttr>', crud.views.updt_users),
    path('put/comments/<str:id>/<str:attr>/<str:newAttr>', crud.views.updt_comments),
    path('delete/user/<str:id>', crud.views.delete_user),
    path('delete/comment/<str:id>', crud.views.delete_comment),
    path('delete/<str:id>', crud.views.delete_all),
    path('map/<str:lon>/<str:lat>/<int:radius>', crud.views.get_aparcamientos),
    path('map/<str:lon>/<str:lat>', crud.views.get_aparcamiento_cercano),
]
