from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.models import Post, Comment, ChatRoom, Message, Friend, Notification


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        help_text='Required',
        required=True
    )
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']

    title = forms.CharField(
        max_length=100,
        required=True,
    )

    content = forms.Textarea()
