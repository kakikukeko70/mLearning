from django.urls import path, include
from .views import Accounts, SignUpView, ActivateView 

app_name = 'accounts'
urlpatterns = [
    path('account/', Accounts.as_view(), name='accounts'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/', ActivateView.as_view(), name='activate'),
]