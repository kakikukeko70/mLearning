from django.views.generic.base import TemplateView
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render

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

class FolderDetailView(DetailView):
    model = Folder
    template_name = 'main/folder_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark_form'] = BookmarkForm() 
        context['folder_form'] = FolderForm()
        context['bookmarks'] = Bookmark.objects.filter(user=self.request.user.id)
        return context
    
    def post(self, request, **kwargs):
        if 'add_bookmark' in request.POST:
            bookmark_form = BookmarkForm(request.POST)
            if bookmark_form.is_valid():
                folder = Folder.objects.get(id=kwargs['pk'])
                Bookmark.objects.create(
                    name=bookmark_form.cleaned_data['name'], 
                    url=bookmark_form.cleaned_data['url'], 
                    user=request.user,
                    folder=folder)
            else:
                context = {
                    'folder': Folder.objects.get(id=kwargs['pk']),
                    'bookmark_form': bookmark_form,
                    'folder_form': FolderForm(),
                    'bookmarks': Bookmark.objects.filter(user=self.request.user.id)
                }
                return render(request, 'main/folder_detail.html', context)
        return redirect('main:folder_detail', pk=self.kwargs['pk'])

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