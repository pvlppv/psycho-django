from django.urls import path, include
from . import views
from .views import MainView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(MainView.as_view()), name='main'),
    # path('', views.main, name='main')
]