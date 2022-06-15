from datetime import date

from django.views.generic.base import TemplateView
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from accounts.models import Memo, Todo
from accounts.forms import MemoForm, TodoForm

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
      
class UpdateMemoView(UpdateView):
    model = Memo
    fields = ['memo']
    success_url = reverse_lazy('main:index')
    
    def form_invalid(self, form):
        return redirect('main:error')

class CreateTodoView(CreateView):
    model = Todo
    fields = ['text', 'deadline']
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('main:error')

class SwitchDoneview(UpdateView):
    model = Todo
    fields = ['done']
    success_url = reverse_lazy('main:index')