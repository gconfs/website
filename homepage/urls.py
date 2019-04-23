from django.urls import path, include

from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('talks/', views.TalkListView.as_view(), name='talk'),
    path('team/', views.TeamView.as_view(), name='team'),
]
