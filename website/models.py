from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.IntegerField(default=0)
    disliked = models.IntegerField(default=0)
    commented = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ChatRoom(models.Model):
    class Type(models.TextChoices):
        PRIVATE = 'private'
        GROUP = 'group'

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20, choices=Type.choices, default=Type.PRIVATE)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " - " + self.chatroom.name


class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Friend(models.Model):
    class stateRequest(models.TextChoices):
        PENDING = 'pending'
        ACCEPTED = 'accepted'
        REJECTED = 'rejected'
        BLOCKED = 'blocked'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user'

    )
    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend'
    )

    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, null=False)

    state = models.CharField(
        max_length=20, choices=stateRequest.choices,
        default=stateRequest.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.post.title}'


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.post.title}'


class Notification(models.Model):
    class typeNotification(models.TextChoices):
        FRIEND_REQUEST = 'friend_request'
        FRIEND_ACCEPTED = 'friend_accepted'
        FRIEND_REJECTED = 'friend_rejected'
        FRIEND_BLOCKED = 'friend_blocked'
        MESSAGE_RECEIVED = 'message_received'
        COMMENT_RECEIVED = 'comment_received'
        LIKE_RECEIVED = 'like_received'
        DISLIKE_RECEIVED = 'dislike_received'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_notification')

    notification_type = models.CharField(
        max_length=20, choices=typeNotification.choices)

    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='message_notification', null=True)

    friend = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='friend_notification', null=True)

    like = models.ForeignKey(
        Like, on_delete=models.CASCADE, related_name='like_notification', null=True)

    dislike = models.ForeignKey(
        Dislike, on_delete=models.CASCADE, related_name='dislike_notification', null=True)

    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='comment_notification', null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
