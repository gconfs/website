from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from dashboard.models import Video

# Create your views here.

class HomePageView(ListView):

    model = Video
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TalkListView(ListView):

    model = Video
    template_name = "talk_list.html"
    paginate_by = 50
    ordering = ['-date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
