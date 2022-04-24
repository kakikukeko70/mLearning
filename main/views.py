from re import template
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect 
from django.shortcuts import get_object_or_404
from accounts.models import User, Bookmark, Folder
from accounts.forms import MemoForm, BookmarkForm, FolderForm

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memo_form'] = MemoForm() 
        return context

class TodoListView(TemplateView):
    template_name = 'main/todo.html'
    
class BookmarksView(TemplateView):
    template_name = 'main/bookmarks.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_form'] = FolderForm()
        return context

class EditBookmark(DetailView):
    model = Bookmark
    template_name = 'main/edit_bookmark.html'
    
class FolderdetailView(DetailView):
    model = Folder
    template_name = 'main/folder_detail.html'
    
    def post(self, request, *arg, **kwargs):
        user = User(pk=request.user.id)
        bookmark_form = BookmarkForm(request.POST)
        folder_name = request.POST['folder']
        folder = Folder.objects.get(name=folder_name)
        if bookmark_form.is_valid():
            bookmark = bookmark_form.save(commit=False)
            bookmark.user = user
            bookmark.folder = folder
            bookmark.save()
            return HttpResponseRedirect(reverse('main:bookmarks'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark_form'] = BookmarkForm()
        context['bookmarks'] = Bookmark.objects.filter(user=self.request.user.id)
        return context
    
def upload_memo(request):
    form = MemoForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        user = get_object_or_404(User, pk=request.user.id)
        user.memo = content
        user.save()
        return HttpResponseRedirect(reverse('main:index'))
    
def create_folder(request):
    user = User(pk=request.user.id)
    form = FolderForm(request.POST)
    if form.is_valid():
        folder = form.save(commit=False)
        folder.user = user
        folder.save()
        return HttpResponseRedirect(reverse('main:bookmarks'))