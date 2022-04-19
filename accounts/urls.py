from django.urls import path, include
from .views import Accounts

app_name = 'accounts'
urlpatterns = [
    path('account/', Accounts.as_view(), name='accounts'),
]