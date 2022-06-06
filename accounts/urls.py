from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('account/', views.AccountView.as_view(), name='account'),
    path('change_username/<int:pk>/', views.CangeUserNameView.as_view(), name='change_username'),
    path('testuser_login/', views.testuser_login, name='testuser_login'),
    path('delete_account/<int:pk>/', views.UserDeleteView.as_view(), name='delete_account'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('email_sent/', views.VerifyView.as_view(), name='verify'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('password_change/', views.ChangedTemplatePasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.ChangedTemplatePasswordResetView.as_view(), name='password_reset'),
]