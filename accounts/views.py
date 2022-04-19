from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class Accounts(TemplateView):
    template_name = 'accounts/accounts.html'