from django.views.generic.base import TemplateView
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from accounts.models import Bookmark, Folder
from accounts.forms import BookmarkForm, FolderForm

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

class FolderdetailView(DetailView):
    model = Folder
    template_name = 'main/folder_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark_form'] = BookmarkForm()
        context['folder_form'] = FolderForm()
        context['bookmarks'] = Bookmark.objects.filter(user=self.request.user.id)
        return context
    

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