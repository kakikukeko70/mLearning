from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import Index, TodoList, upload_memo


app_name='main'
urlpatterns = [
    path('', login_required(Index.as_view()), name='index'),
    path('todo/', TodoList.as_view(), name='todo'),
    path('upload_memo>/', upload_memo, name='upload_memo'),
]