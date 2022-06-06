from django.views.generic.base import TemplateView

class ErrorView(TemplateView):
    template_name = 'error/error.html'

class InvalidUrlView(TemplateView):
    template_name = 'error/invalid_url.html'