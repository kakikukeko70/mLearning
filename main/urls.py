from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import Index, TodoList


app_name='main'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('todo/', TodoList.as_view(), name='todo'),
]