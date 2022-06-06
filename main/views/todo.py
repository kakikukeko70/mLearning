from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from accounts.models import Todo
from accounts.forms import TodoForm

class TodosView(ListView):
    model = Todo
    template_name = 'main/todos.html'
    
    def get_queryset(self):
        return Todo.objects.order_by('deadline')

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
    fields = ['text']
    success_url = reverse_lazy('main:todos')

    def form_invalid(self, form):
        return redirect('main:error')

class DeleteTodoView(DeleteView):
    model = Todo    
    success_url = reverse_lazy('main:todos')

class SwitchDoneview(UpdateView):
    model = Todo
    fields = ['done']
    success_url = reverse_lazy('main:todos')