from django.urls import path, include
from .views import AccountView, CangeUserNameView, UserDeleteView, SignUpView, ActivateView, VerifyView

app_name = 'accounts'
urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('change_username/<int:pk>/', CangeUserNameView.as_view(), name='change_username'),
    path('testuser_login', AccountView.testuser_login, name='testuser_login'),
    path('delete_account/<int:pk>/', UserDeleteView.as_view(), name='delete_account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('email_sent/', VerifyView.as_view(), name='verify'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]