from datetime import date

from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView
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
      
class CreateTodoView(CreateView):
    model = Todo
    fields = ['text', 'deadline']
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('main:error')

class UpdateMemoView(UpdateView):
    model = Memo
    fields = ['memo']
    success_url = reverse_lazy('main:index')
    
    def form_invalid(self, form):
        return redirect('main:error')

class ChangeDoneview(UpdateView):
    model = Todo
    fields = ['done']
    success_url = reverse_lazy('main:index')

class FolderView(TemplateView):
    template_name = 'main/folders.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_form'] = FolderForm()
        return context

class CreateFolderView(CreateView):
    model = Folder
    fields = ['name']
    success_url = reverse_lazy('main:folders')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('main:error')

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
    
    # def add_bookmark(request, **kwargs):
    #     folder = Folder.objects.get(id=kwargs['id'])
    #     user = User(pk=request.user.id)
    #     bookmark_form = BookmarkForm(request.POST)
    #     if bookmark_form.is_valid():
    #         bookmark = bookmark_form.save(commit=False)
    #         bookmark.user = user
    #         bookmark.folder = folder
    #         bookmark.save()
    #         return HttpResponseRedirect(reverse('main:folder_detail', kwargs={'pk' : kwargs['id']})) 
    #     return HttpResponseRedirect(reverse('main:error'))

class CreateBookmarkView(CreateView):
    model = Bookmark
    fields = ['name', 'url']

    def get_success_url(self):
        return reverse('main:folder_detail', kwargs={'pk': self.kwargs['id']})

    def form_valid(self, form):
        folder = Folder.objects.get(id=self.kwargs['id'])
        form.instance.folder = folder
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChangeFolderName(UpdateView):
    model = Folder
    fields = ['name']

    def get_success_url(self):
        return reverse('main:folder_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        return redirect('main:error')

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

class UpdateTodoView(UpdateView):
    model = Todo
    success_url = reverse_lazy('main:todos')

    def form_invalid(self, form):
        return redirect('main:error')

class DeleteTodoView(DeleteView):
    model = Todo    
    success_url = reverse_lazy('main:todos')

class TodosView(ListView):
    model = Todo
    template_name = 'main/todos.html'
    
    def get_queryset(self):
        return Todo.objects.order_by('deadline')

class SwitchDoneview(UpdateView):
    model = Todo
    fields = ['done']
    success_url = reverse_lazy('main:todos')
       
class ErrorView(TemplateView):
    template_name = 'error/error.html'