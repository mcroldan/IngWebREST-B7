
from django.urls import path
import crud.views

urlpatterns = [
    path('test', crud.views.main),
    path('list_users', crud.views.get_all_users),
    path('list_comments', crud.views.get_all_comments)
]
