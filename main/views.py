from datetime import date

from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.http import HttpResponseRedirect 
from django.shortcuts import get_object_or_404

from accounts.models import User, Bookmark, Folder, Todo
from accounts.forms import MemoForm, BookmarkForm, FolderForm, BookmarkNameForm, TodoForm 

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = Todo.objects.filter(user=self.request.user)
        memo_form = MemoForm()
        memo_form.fields['memo'].initial = self.request.user.memo
        context['memo_form'] = memo_form
        context['todos'] = todo.filter(deadline__gte=date.today()).order_by('deadline')
        context['overdues'] = todo.filter(deadline__lt=date.today(), done=False).order_by('deadline')
        return context

    def upload_memo(request):
        form = MemoForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['memo']
            user = get_object_or_404(User, pk=request.user.id)
            user.memo = content
            user.save()
            return HttpResponseRedirect(reverse('main:index'))
        return HttpResponseRedirect(reverse('main:error'))

    def add_todo(request):
        todo_form = TodoForm(request.POST) 
        if todo_form.is_valid():
            user = User.objects.get(pk=request.user.id)
            todo = Todo.objects.create(
            text=todo_form.cleaned_data['text'], 
            deadline=todo_form.cleaned_data['deadline'],
            user=user)
            return HttpResponseRedirect(reverse('main:index'))
        return HttpResponseRedirect(reverse('main:error'))
      
    def update_todo(request, **kwargs):
       is_done = request.POST.get(f"is_done_{kwargs['pk']}")
       todo = Todo.objects.get(pk=kwargs['pk'])
       if is_done:
           todo.done = True
       else:
           todo.done = False
       todo.save()
       return HttpResponseRedirect(reverse('main:index'))
    
class FolderView(TemplateView):
    template_name = 'main/folders.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_form'] = FolderForm()
        return context

    def create_folder(request):
        user = User(pk=request.user.id)
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = user
            folder.save()
            return HttpResponseRedirect(reverse('main:folders'))
        return HttpResponseRedirect(reverse('main:error'))

class EditBookmark(DetailView):
    model = Bookmark
    template_name = 'main/edit_bookmark.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark_name_form'] = BookmarkNameForm()
        return context

    def change_bookmark_name(request, **kwargs):
        bookmark_name_form = BookmarkNameForm(request.POST)
        if bookmark_name_form.is_valid():
            bookmark_name = bookmark_name_form.cleaned_data['name']
            bookmark = Bookmark.objects.get(id=kwargs['id'])
            bookmark.name = bookmark_name
            bookmark.save()
            return HttpResponseRedirect(reverse('main:editbookmark', kwargs={'pk' : kwargs['id']})) 
        return HttpResponseRedirect(reverse('main:error'))
            
    def change_folder(request, **kwargs):
        folder_name = request.POST['folder']
        bookmark = Bookmark.objects.get(id=kwargs['id'])
        folder = Folder.objects.get(name=folder_name)
        bookmark.folder = folder
        bookmark.save()
        return HttpResponseRedirect(reverse('main:editbookmark', kwargs={'pk' : kwargs['id']})) 
    
    def delete_bookmark(request, **kwargs):
        bookmark = Bookmark.objects.get(id=kwargs['id'])
        bookmark.delete()
        folder_pk = bookmark.folder.id
        return HttpResponseRedirect(reverse('main:folderdetail', kwargs={'pk' : folder_pk})) 

class FolderdetailView(DetailView):
    model = Folder
    template_name = 'main/folder_detail.html'
    
    def add_bookmark(request, **kwargs):
        folder = Folder.objects.get(id=kwargs['id'])
        user = User(pk=request.user.id)
        bookmark_form = BookmarkForm(request.POST)
        if bookmark_form.is_valid():
            bookmark = bookmark_form.save(commit=False)
            bookmark.user = user
            bookmark.folder = folder
            bookmark.save()
            return HttpResponseRedirect(reverse('main:folderdetail', kwargs={'pk' : kwargs['id']})) 
        return HttpResponseRedirect(reverse('main:error'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark_form'] = BookmarkForm()
        context['folder_form'] = FolderForm()
        context['bookmarks'] = Bookmark.objects.filter(user=self.request.user.id)
        return context
    
    def change_folder_name(request, **kwargs):
        folder_form = FolderForm(request.POST)
        if folder_form.is_valid():
            folder = Folder.objects.get(id=kwargs['id'])
            folder_name = folder_form.cleaned_data['name']
            folder.name = folder_name
            folder.save()
            return HttpResponseRedirect(reverse('main:folderdetail', kwargs={'pk' : kwargs['id']})) 
        return HttpResponseRedirect(reverse('main:error'))

    def delete_folder(request, **kwargs):
        folder = Folder.objects.get(id=kwargs['id'])
        folder.delete()
        return HttpResponseRedirect(reverse('main:folders'))

class TodoEditView(DetailView):
    model = Todo
    template_name = 'main/todo_edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = Todo.objects.get(text=kwargs['object'])
        context['deadline'] = todo.deadline.isoformat()
        return context
    
    def update_todo(request, **kwargs):
        todo = Todo.objects.get(pk=kwargs['pk'])
        todo_form = TodoForm(request.POST, instance=todo)
        if todo_form.is_valid():
            todo_form.save()
            return HttpResponseRedirect(reverse('main:index'))
        return HttpResponseRedirect(reverse('main:error'))

    
    def delete_todo(request, **kwargs):
        todo = Todo.objects.get(pk=kwargs['pk'])
        todo.delete()
        return HttpResponseRedirect(reverse('main:index'))

class TodosView(ListView):
    model = Todo
    template_name = 'main/todos.html'
    
    def get_queryset(self):
        return Todo.objects.order_by('deadline')

    def update_todo(request, **kwargs):
       is_done = request.POST.get(f"is_done_{kwargs['pk']}")
       todo = Todo.objects.get(pk=kwargs['pk'])
       if is_done:
           todo.done = True
       else:
           todo.done = False
       todo.save()
       return HttpResponseRedirect(reverse('main:todos'))
       
class ErrorView(TemplateView):
    template_name = 'error/error.html'