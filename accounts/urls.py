from django.urls import path, include
from .views import AccountView, SignUpView, ActivateView, VerifyView 

app_name = 'accounts'
urlpatterns = [
    path('account/', AccountView.as_view(), name='accounts'),
    path('change_username', AccountView.change_username, name='change_username'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('email_sent/', VerifyView.as_view(), name='verify'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]