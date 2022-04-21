from django.shortcuts import render
from django.views.generic.base import TemplateView

class Index(TemplateView):
    template_name = 'main/index.html'

class TodoList(TemplateView):
    template_name = 'main/todo.html'