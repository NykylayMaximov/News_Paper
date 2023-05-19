from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'Posts.html'
    context_object_name = 'posts'


class PostDateil(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'