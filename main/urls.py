from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import Index


app_name='main'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('', include('accounts.urls')),
]