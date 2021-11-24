from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
import crud.views

urlpatterns = [
    url(r'map', views.default_map, name="default"),
    path('test', crud.views.main),
    path('list_users', crud.views.get_all_users),
    path('list_comments', crud.views.get_all_comments)
]
