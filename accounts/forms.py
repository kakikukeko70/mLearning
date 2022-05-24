from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django import forms
from .models import User, Bookmark, Folder, Todo

User = get_user_model()

class MemoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('memo',)
        labels = {
            'memo': '',
        }

class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'})
        }
    
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('name', 'url')

class BookmarkNameForm(forms.ModelForm):
   class Meta:
       model = Bookmark
       fields = ('name',) 

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('text', 'deadline')
        Widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        
subject = "Your account is up and running!"
message_template = """
We’d like to confirm that your account was created successfully. 
To access account, go to the link below.
"""

def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + "/activate/{}/{}/".format(uid, token)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        user.is_active = False
        
        if commit:
            user.save()
            activate_url = get_activate_url(user)
            message = message_template + activate_url
            user.email_user(subject, message)
        return user
        

def activate_user(uidb64, token):    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return False

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    
    return False