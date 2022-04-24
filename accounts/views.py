from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect 
from django.urls import reverse
from .models import User
from .forms import SignUpForm, activate_user, UserNameForm

# Create your views here.
class AccountView(TemplateView):
    template_name = 'accounts/accounts.html'

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:verify')
    template_name = 'accounts/signup.html'
    
class VerifyView(TemplateView):
    template_name = 'accounts/verify.html'
    
class ActivateView(TemplateView):
    template_name = "accounts/activate.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        result = activate_user(uidb64, token)
        return super().get(request, result=result, **kwargs)

def change_username(request):
    form = UserNameForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        user = get_object_or_404(User, pk=request.user.id)
        user.username = username
        user.save()   
        return HttpResponseRedirect(reverse('main:index'))