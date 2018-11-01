from django.urls import path, include

from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
]
