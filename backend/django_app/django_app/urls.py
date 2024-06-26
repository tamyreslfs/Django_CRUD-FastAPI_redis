from django.urls import path
from django.views.generic import RedirectView
from django.http import HttpResponse


# Uma view simples para a página inicial
def home(request):
    return HttpResponse("Hello, world!")


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('', home),  # Adiciona uma rota para a URL raiz
]
