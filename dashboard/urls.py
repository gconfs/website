from django.urls import path, include

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('generator/', views.GeneratorView.as_view(), name='generator'),
    path('events/', views.EventsView.as_view(), name='events'),
]
