from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from website.forms import *
from website.models import *
from Logging.Logger_Base import log


# Create your views here.


class HomeView(UserPassesTestMixin, TemplateView):
    template_name = 'website/home.html'
    group_required = ['default', 'sudo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_objs = Post.objects.all()
        posts = []

        for post in posts_objs:
            posts.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "liked": post.liked,
                    "disliked": post.disliked,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at,
                    "author": post.author,
                    "like": True if Like.objects.select_related('post').filter(user=self.request.user, post=post) else False,
                    "dislike": True if Dislike.objects.select_related('post').filter(user=self.request.user, post=post) else False
                }
            )

        context['posts'] = posts

        return context

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.group_required).exists()


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='default')
        user.groups.add(group)
        if user is not None:
            login(self.request, user)
            log.info(f'New user {user.username} registered')
            messages.success(self.request, 'Registration successful')
        return super().form_valid(form)

    def get(self, request, *args: str, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class PostView(PermissionRequiredMixin, CreateView):
    template_name = 'website/post.html'
    form_class = PostForm
    context_object_name = 'post'
    permission_required = 'website.add_post'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully')
        log.info(f'New post created by {self.request.user.username}')
        return super().form_valid(form)


class DeletePostView(PermissionRequiredMixin, DeleteView):
    template_name = 'website/delete_post.html'
    model = Post
    permission_required = 'website.delete_post'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Post deleted successfully')
        log.info(f'Post deleted by {self.request.user.username}')
        return super().form_valid(form)


class BanUserView(UserPassesTestMixin, TemplateView):
    template_name = 'website/ban_user.html'

    def test_func(self):
        return self.request.user.groups.filter(name='sudo').exists()

    def get(self, request, *args: str, **kwargs):
        if self.test_func():
            return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, 'You are not allowed to do that')
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_to_ban'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args: str, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        try:
            group = Group.objects.get(name='default')
            group.user_set.remove(user)
        except:
            pass

        try:
            group = Group.objects.get(name='sudo')
            group.user_set.remove(user)
        except:
            pass

        messages.success(self.request, 'User banned successfully')
        log.info(
            f'User {user.username} banned by {self.request.user.username}')

        return redirect('home')


class UnbanUserView(UserPassesTestMixin, TemplateView):
    template_name = 'website/unban_user.html'

    def test_func(self):
        return self.request.user.groups.filter(name='sudo').exists()

    def get(self, request, *args: str, **kwargs):
        if self.test_func():
            return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, 'You are not allowed to do that')
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_to_unban'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args: str, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        group = Group.objects.get(name='default')
        user.groups.add(group)

        messages.success(self.request, 'User unbanned successfully')
        log.info(
            f'User {user.username} unbanned by {self.request.user.username}')
        return redirect('home')


def postLiked(request, pk):
    post = Post.objects.get(id=pk)
    if Like.objects.select_related('user').filter(user=request.user, post=post):
        Like.objects.select_related('user').filter(
            user=request.user, post=post).delete()
        post.liked -= 1
        post.save()
    elif Dislike.objects.select_related('user').filter(user=request.user, post=post):
        Dislike.objects.select_related('user').filter(
            user=request.user, post=post).delete()
        post.disliked -= 1
        Like.objects.create(user=request.user, post=post)
        post.liked += 1
        post.save()
    else:
        Like.objects.create(user=request.user, post=post)
        post.liked += 1
        post.save()

    return redirect('home')


def postDisliked(request, pk):
    post = Post.objects.get(id=pk)
    if Dislike.objects.select_related('user').filter(user=request.user, post=post):
        Dislike.objects.select_related('user').filter(
            user=request.user, post=post).delete()
        post.disliked -= 1
        post.save()
    elif Like.objects.select_related('user').filter(user=request.user, post=post):
        Like.objects.select_related('user').filter(
            user=request.user, post=post).delete()
        post.liked -= 1
        Dislike.objects.create(user=request.user, post=post)
        post.disliked += 1
        post.save()
    else:
        Dislike.objects.create(user=request.user, post=post)
        post.disliked += 1
        post.save()

    return redirect('home')
