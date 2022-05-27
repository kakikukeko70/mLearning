from datetime import date

from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect 
from django.shortcuts import get_object_or_404, redirect

from accounts.models import User, Memo, Bookmark, Folder, Todo
from accounts.forms import MemoForm, BookmarkForm, FolderForm, BookmarkNameForm, TodoForm

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memo = Memo.objects.get(user=self.request.user)
        memo_form = MemoForm()
        memo_form.fields['memo'].initial = memo.memo
        context['memo_form'] = memo_form
        context['todo_form'] = TodoForm()
        todo = Todo.objects.filter(user=self.request.user)
        context['todos'] = todo.filter(deadline__gte=date.today()).order_by('deadline')
        context['overdues'] = todo.filter(deadline__lt=date.today(), done=False).order_by('deadline')
        return context

    def update_memo(request):
        form = MemoForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['memo']
            user = get_object_or_404(User, pk=request.user.id)
            user.memo = content
            user.save()
            return HttpResponseRedirect(reverse('main:index'))
        return HttpResponseRedirect(reverse('main:error'))

    def add_todo(request):
        form = TodoForm(request.POST) 
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            todo = Todo.objects.create(
                text=form.cleaned_data['text'], 
                deadline=form.cleaned_data['deadline'],
                user=user)
            return HttpResponseRedirect(reverse('main:index'))
        return HttpResponseRedirect(reverse('main:error'))
      
    def switch_done(request, **kwargs):
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

class ChangeBookmarkName(UpdateView):
    model = Bookmark
    fields = ['name']

    def get_success_url(self):
        return reverse('main:edit_bookmark', kwargs={'pk': self.object.pk})
    
    def form_invalid(self,form):
        return redirect('main:error')

class ChangeFolderView(UpdateView):
    model = Folder
    fields = ['folder']

    def get_success_url(self):
        return reverse('main:edit_bookmark', kwargs={'pk': self.object.pk})

class DeleteBookmarkView(DeleteView):
    model = Bookmark

    def get_success_url(self):
        bookmark = Bookmark.objects.get(id=self.object.pk)
        folder_pk = bookmark.folder.pk
        return reverse('main:folder_detail', kwargs={'pk': folder_pk})

class FolderdetailView(DetailView):
    model = Folder
    template_name = 'main/folder_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark_form'] = BookmarkForm()
        context['folder_form'] = FolderForm()
        context['bookmarks'] = Bookmark.objects.filter(user=self.request.user.id)
        return context
    
    def add_bookmark(request, **kwargs):
        folder = Folder.objects.get(id=kwargs['id'])
        user = User(pk=request.user.id)
        bookmark_form = BookmarkForm(request.POST)
        if bookmark_form.is_valid():
            bookmark = bookmark_form.save(commit=False)
            bookmark.user = user
            bookmark.folder = folder
            bookmark.save()
            return HttpResponseRedirect(reverse('main:folder_detail', kwargs={'pk' : kwargs['id']})) 
        return HttpResponseRedirect(reverse('main:error'))

    def change_folder_name(request, **kwargs):
        folder_form = FolderForm(request.POST)
        if folder_form.is_valid():
            folder_name = folder_form.cleaned_data['name']
            folder = Folder.objects.get(id=kwargs['id'])
            folder.name = folder_name
            folder.save()
            return HttpResponseRedirect(reverse('main:folderdetail', kwargs={'pk' : kwargs['id']})) 
        return HttpResponseRedirect(reverse('main:error'))

class DeleteFolderView(DeleteView):
    model = Folder
    success_url = reverse_lazy('main:folders')

class EditTodoView(DetailView):
    model = Todo
    template_name = 'main/edit_todo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = Todo.objects.get(text=kwargs['object'])
        update_todo_form = TodoForm()
        update_todo_form.fields['deadline'].initial = todo.deadline.isoformat()
        update_todo_form.fields['text'].initial = todo.text
        context['update_todo_form'] = update_todo_form
        return context
    
    def update_todo(request, **kwargs):
        todo = Todo.objects.get(pk=kwargs['pk'])
        todo_form = TodoForm(request.POST, instance=todo)
        if todo_form.is_valid():
            todo_form.save()
            return HttpResponseRedirect(reverse('main:todos'))
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

    def change_done(request, **kwargs):
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