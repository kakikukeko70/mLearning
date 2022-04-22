from django.urls import path, include
from .views import Accounts, SignUpView, ActivateView, Verify 

app_name = 'accounts'
urlpatterns = [
    path('account/', Accounts.as_view(), name='accounts'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('email_sent/', Verify.as_view(), name='verify'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]