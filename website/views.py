from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'website/home.html'
