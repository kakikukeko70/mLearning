from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

app_name='main'
urlpatterns = [
    path('', login_required(views.IndexView.as_view()), name='index'),
    path('update_memo/<int:pk>/', views.UpdateMemoView.as_view(), name='update_memo'),
    path('add_todo/', views.CreateTodoView.as_view(), name='add_todo'),
    path('switch_done/<int:pk>/', views.ChangeDoneview.as_view(), name='switch_done'),
    path('bookmark_folders/', views.FolderView.as_view(), name='folders'),
    path('create_folder/', views.CreateFolderView.as_view(), name='create_folder'),
    path('edit_bookmark/<int:pk>/', views.EditBookmark.as_view(), name='edit_bookmark'),
    path('change_bookmark/<int:pk>/', views.ChangeBookmarkName.as_view(), name='change_bookmark_name'),
    path('change_folder/<int:id>/', views.ChangeFolderView.as_view(), name='change_folder'),
    path('delete_bookmark/<int:pk>/', views.DeleteBookmarkView.as_view(), name='delete_bookmark'),
    path('folder_detail/<int:pk>/', views.FolderdetailView.as_view(), name='folder_detail'),
    path('add_bookmark/<int:id>/', views.CreateBookmarkView.as_view(), name='add_bookmark'),
    path('change_foldername/<int:pk>/', views.ChangeFolderName.as_view(), name='change_folder_name'),
    path('delete_folder/<int:pk>/', views.DeleteFolderView.as_view(), name='delete_folder'),
    path('edit_todo/<int:pk>/', views.EditTodoView.as_view(), name='edit_todo'),
    path('update_todo/<int:pk>/', views.UpdateTodoView.as_view(), name='update_todo'),
    path('delete_todo/<int:pk>/', views.DeleteTodoView.as_view(), name='delete_todo'),
    path('todos/', views.TodosView.as_view(), name='todos'), 
    path('change_done/<int:pk>/', views.SwitchDoneview.as_view(), name='change_done'),
    path('error/', views.ErrorView.as_view(), name='error'),
]