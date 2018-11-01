from django.urls import path, include

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('eventgen/', views.EventGenView.as_view(), name='eventgen'),
]
