from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import IndexView, TodoListView, FolderView, EditBookmark, FolderdetailView

app_name='main'
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('todo/', TodoListView.as_view(), name='todo'),
    path('bookmark_folders/', FolderView.as_view(), name='folders'),
    path('edit_bookmark/<int:pk>/', EditBookmark.as_view(), name='editbookmark'),
    path('folderdetail/<int:pk>', FolderdetailView.as_view(), name='folderdetail'),
    path('upload_memo/', IndexView.upload_memo, name='upload_memo'),
    path('create_folder/', FolderView.create_folder, name='create_folder'),
    path('change_bookmark_name/<int:id>/', EditBookmark.change_bookmark_name, name='change_bookmark_name'),
    path('change_folder/<int:id>/', EditBookmark.change_folder, name='change_folder'),
    path('delete_bookmark/<int:id>', EditBookmark.delete_bookmark, name='delete_bookmark'),
]