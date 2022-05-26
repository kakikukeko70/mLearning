from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import IndexView, EditTodoView, FolderView, EditBookmark, FolderdetailView, TodosView, ErrorView

app_name='main'
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('update_memo/', IndexView.update_memo, name='update_memo'),
    path('add_todo/', IndexView.add_todo, name='add_todo'),
    path('switch_done/<int:pk>/', IndexView.swith_done, name='switch_done'),
    path('bookmark_folders/', FolderView.as_view(), name='folders'),
    path('create_folder/', FolderView.create_folder, name='create_folder'),
    path('edit_bookmark/<int:pk>/', EditBookmark.as_view(), name='editbookmark'),
    path('change_bookmark/<int:id>', EditBookmark.change_bookmark_name, name='change_bookmark_name'),
    path('change_folder/<int:id>/', EditBookmark.change_folder, name='change_folder'),
    path('delete_bookmark/<int:id>/', EditBookmark.delete_bookmark, name='delete_bookmark'),
    path('folder_detail/<int:pk>', FolderdetailView.as_view(), name='folder_detail'),
    path('add_bookmark/<int:id>', FolderdetailView.add_bookmark, name='add_bookmark'),
    path('change_foldername/<int:id>/', FolderdetailView.change_folder_name, name='change_folder_name'),
    path('delete_folder/<int:id>/', FolderdetailView.delete_folder, name='delete_folder'),
    path('edit_todo/<int:pk>/', EditTodoView.as_view(), name='edit_todo'),
    path('update_todo/<int:pk>/', EditTodoView.update_todo, name='update_todo'),
    path('delete_todo/<int:pk>/', EditTodoView.delete_todo, name='delete_todo'),
    path('todos/', TodosView.as_view(), name='todos'), 
    path('change_done/<int:pk>/', TodosView.change_done, name='change_done'),
    path('error/', ErrorView.as_view(), name='error'),
]