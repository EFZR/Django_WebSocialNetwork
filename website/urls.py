from django.urls import path
from website import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('post/', views.PostView.as_view(), name='post'),
    path('delete_post/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('friends/', views.FriendsView.as_view(), name='friends'),
    path('add_friends/', views.AddFriendsView.as_view(), name='add_friends'),
    path('accept_friend/<int:pk>/<int:nt_pk>/', views.aceceptFriendRequest, name='accept_friend'),
    path('decline_friend/<int:pk>/<int:nt_pk>/', views.declineFriendRequest, name='decline_friend'),
    path('chat/<int:chatroom_id>', views.ChatroomView.as_view(), name='chat'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('checked_notification/<int:pk>/', views.checkedNotification, name='checked_notification'),
    path('ban_user/<int:pk>/', views.BanUserView.as_view(), name='ban_user'),
    path('unban_user/<int:pk>/', views.UnbanUserView.as_view(), name='unban_user'),
    path('like/<int:pk>/<int:author>/', views.postLiked, name='like'),
    path('dislike/<int:pk>/<int:author>/', views.postDisliked, name='dislike'),
    path('comment/<int:pk>/<int:author>/', views.CommentView.as_view(), name='comment'),
]
