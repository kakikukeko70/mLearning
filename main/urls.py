from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import index, todo, bookmark, folder, error

app_name='main'
urlpatterns = [
    path('', login_required(index.IndexView.as_view()), name='index'),
    path('update_memo/<int:pk>/', index.UpdateMemoView.as_view(), name='update_memo'),
    path('add_todo/', index.CreateTodoView.as_view(), name='add_todo'),
    path('switch_done/<int:pk>/', index.ChangeDoneview.as_view(), name='switch_done'),
    path('bookmark_folders/', folder.FolderView.as_view(), name='folders'),
    path('create_folder/', folder.CreateFolderView.as_view(), name='create_folder'),
    path('change_foldername/<int:pk>/', folder.ChangeFolderName.as_view(), name='change_folder_name'),
    path('delete_folder/<int:pk>/', folder.DeleteFolderView.as_view(), name='delete_folder'),
    path('folder_detail/<int:pk>/', folder.FolderDetailView.as_view(), name='folder_detail'),
    path('add_bookmark/<int:id>/', folder.CreateBookmarkView.as_view(), name='add_bookmark'),
    path('edit_bookmark/<int:pk>/', bookmark.EditBookmark.as_view(), name='edit_bookmark'),
    path('change_bookmark/<int:pk>/', bookmark.ChangeBookmarkName.as_view(), name='change_bookmark_name'),
    path('change_folder/<int:id>/', bookmark.ChangeFolderView.as_view(), name='change_folder'),
    path('delete_bookmark/<int:pk>/', bookmark.DeleteBookmarkView.as_view(), name='delete_bookmark'),
    path('edit_todo/<int:pk>/', todo.EditTodoView.as_view(), name='edit_todo'),
    path('update_todo/<int:pk>/', todo.UpdateTodoView.as_view(), name='update_todo'),
    path('delete_todo/<int:pk>/', todo.DeleteTodoView.as_view(), name='delete_todo'),
    path('todos/', todo.TodosView.as_view(), name='todos'), 
    path('change_done/<int:pk>/', todo.SwitchDoneview.as_view(), name='change_done'),
    path('error/', error.ErrorView.as_view(), name='error'),
    path('invalid_url/', error.InvalidUrlView.as_view(), name='invalid_url'),
]