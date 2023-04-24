from django.urls import path
from website import views

urlpatterns= [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('post/', views.PostView.as_view(), name='post'),
    path('like/<int:pk>/', views.postLiked, name='like'),
    path('dislike/<int:pk>/', views.postDisliked, name='dislike')
]