from django.urls import path
from website import views

urlpatterns= [
    path('', views.HomeView.as_view(), name='home'),
]