from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect 
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user_model

from .forms import SignUpForm, activate_user, UserNameForm

User = get_user_model()

class AccountView(TemplateView):
    template_name = 'accounts/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username_form = UserNameForm()
        username_form.fields['username'].initial = self.request.user.username
        context['username_form'] = username_form
        return context

def testuser_login(request):
    user = authenticate(request, username='test', password='testuser')
    login(request, user)
    return HttpResponseRedirect(reverse('main:index'))

class CangeUserNameView(UpdateView):
    model = User
    form_class = UserNameForm
    success_url = reverse_lazy('accounts:account')

    def get_template_names(self):
        if self.request.user.username == 'test':
            return ['accounts/testuser_not_allowed.html']
        return ['accounts/user_form.html']

    def get_initial(self):
        return {"username": self.request.user}
    
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('login')

    def get_template_names(self):
        if self.request.user.username == 'test':
            return ['accounts/testuser_not_allowed.html']
        return ['accounts/user_confirm_delete.html']

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

class ChangedTemplatePasswordChangeView(PasswordChangeView):
    def get_template_names(self):
        if self.request.user.username == 'test':
            return ['accounts/testuser_not_allowed.html']
        return ['registration/password_change_form.html'] 

class ChangedTemplatePasswordResetView(PasswordResetView):
    def get_template_names(self):
        if self.request.user.username == 'test':
            return ['accounts/testuser_not_allowed.html']
        return ['registration/password_reset_form.html'] 