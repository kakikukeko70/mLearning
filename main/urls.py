from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import IndexView, TodoListView, BookmarksView, EditBookmark, FolderdetailView, upload_memo, create_folder

app_name='main'
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('todo/', TodoListView.as_view(), name='todo'),
    path('bookmarks/', BookmarksView.as_view(), name='bookmarks'),
    path('edit_bookmark/<int:pk>/', EditBookmark.as_view(), name='editbookmark'),
    path('folderdetail/<int:pk>', FolderdetailView.as_view(), name='folderdetail'),
    path('upload_memo/', upload_memo, name='upload_memo'),
    path('create_folder/', create_folder, name='create_folder'),
]