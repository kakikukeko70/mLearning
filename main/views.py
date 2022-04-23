from django.views.generic.base import TemplateView
from accounts.forms import MemoForm
from django.urls import reverse
from django.http import HttpResponseRedirect 
from accounts.models import User
from django.shortcuts import get_object_or_404

class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memo_form'] = MemoForm() 
        return context

class TodoList(TemplateView):
    template_name = 'main/todo.html'
    
def upload_memo(request):
    form = MemoForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        user = get_object_or_404(User, pk=request.user.id)
        user.memo = content
        user.save()
        return HttpResponseRedirect(reverse('main:index'))