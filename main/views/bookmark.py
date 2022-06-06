from django.views.generic import DetailView, DeleteView, UpdateView
from django.urls import reverse
from django.shortcuts import redirect

from accounts.models import Bookmark, Folder
from accounts.forms import BookmarkNameForm

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