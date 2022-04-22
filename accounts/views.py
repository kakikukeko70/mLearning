from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import SignUpForm, activate_user

# Create your views here.
class Accounts(TemplateView):
    template_name = 'accounts/accounts.html'

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:verify')
    template_name = 'accounts/signup.html'
    
class Verify(TemplateView):
    template_name = 'accounts/verify.html'
    
class ActivateView(TemplateView):
    template_name = "accounts/activate.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        result = activate_user(uidb64, token)
        return super().get(request, result=result, **kwargs)