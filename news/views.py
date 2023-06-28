from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Post, SubscribeCategory, Category
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.core.mail import send_mail


class PostList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDateil(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.obj = super().get_object(queryset=queryset)
        return self.obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_category'] = self.obj.categories.all()
        if self.request.user.id:
            context['user_subscribers'] = self.request.user.subscribers.all()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def send_mail(self, request):
        post = self.object
        user = request.user
        send_mail(subject=f'{self.post.author}',
                  message=self.post.title,
                  from_email='nick.max89@yandex.ru',
                  recipient_list=['nick.max@mail.ru'])
        return redirect('post_list')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    # login_url = '/posts/'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required()
def subscribe(request, pk, pp):
    user = request.user
    SubscribeCategory.objects.create(subscriber=User.objects.get(pk=user.id),
                                     category=Category.objects.get(pk=pk))
    return redirect(f'/posts/{pp}')


@login_required()
def unsubscribe(request, pk, pp):
    SubscribeCategory.objects.filter(category=Category.objects.get(pk=pk)).delete()
    return redirect(f'/posts/{pp}')
