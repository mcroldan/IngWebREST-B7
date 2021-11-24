
from typing import ValuesView
from django.urls import path
import crud.views

urlpatterns = [
    path('test', crud.views.main),
    path('get/users', crud.views.get_all_users),
    path('get/comments', crud.views.get_all_comments),
    path('get/users/<str:var>', crud.views.get_user),
    path('get/comments/<str:var>', crud.views.get_comment),
    path('post/users/<str:id>/<str:attr>/<str:newAttr>', crud.views.post_users),
    path('post/comments/<str:id>/<str:attr>/<str:newAttr>', crud.views.post_users)
]
