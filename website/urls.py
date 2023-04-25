from django.urls import path
from website import views

urlpatterns= [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('post/', views.PostView.as_view(), name='post'),
    path('delete_post/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('ban_user/<int:pk>/', views.BanUserView.as_view(), name='ban_user'),
    path('unban_user/<int:pk>/', views.UnbanUserView.as_view(), name='unban_user'),
    path('like/<int:pk>/', views.postLiked, name='like'),
    path('dislike/<int:pk>/', views.postDisliked, name='dislike')
]