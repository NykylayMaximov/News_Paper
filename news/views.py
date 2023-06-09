from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Post, SubscribeCategory, Category, PostCategory
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import datetime, timedelta


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

    # def post(self, request, *args, **kwargs):
    #     post = Post(author_id=request.user.id,
    #                 title=request.POST['title'],
    #                 text=request.POST['text'],)
    #     post.save()
    #
    #     category_list = request.POST.getlist('categories')
    #     for category in category_list:
    #         PostCategory.objects.create(post_id=post.id, category_id=category)
    #
    #     return redirect('post_list')

    def post(self, request, *args, **kwargs):
        post_limit_time = datetime.now() - timedelta(hours=24)
        post_count = Post.objects.filter(author_id=request.user.id,
                                         time__gte=post_limit_time).count()
        if post_count >= 3:
            return render(request, 'post_limit_msg.html')
        else:
            post = Post(author_id=request.user.id,
                        title=request.POST['title'],
                        text=request.POST['text'],)
            post.save()

            category_list = request.POST.getlist('categories')
            link = 'http://' + request.META["HTTP_HOST"] + f'/posts/{post.id}'
            user_id_list = []
            user_subscriber_list = []
            user_email_dict = {}
            for category in category_list:
                PostCategory.objects.create(post_id=post.id, category_id=category)
                user_id_list += SubscribeCategory.objects.filter(category_id=category).values('subscriber__id')

            for user in user_id_list:
                if user['subscriber__id'] not in user_subscriber_list and int(user['subscriber__id']) != request.user.id:
                    user_subscriber_list.append(user['subscriber__id'])

            for id in user_subscriber_list:
                subscribe_user = User.objects.get(pk=id)
                user_email_dict[subscribe_user.username] = subscribe_user.email

            if user_email_dict:
                for user_name, email in user_email_dict.items():
                    html_content = render_to_string('post_send_email.html', {'post': post,
                                                                             'user_name': user_name,
                                                                             'link': link
                                                                             }
                                                    )
                    msg = EmailMultiAlternatives(
                        subject=post.title,
                        from_email='nick.max89@gmail.com',
                        to=[email]
                    )
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()

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
    user = request.user
    SubscribeCategory.objects.filter(category=Category.objects.get(pk=pk), subscriber=user.id).delete()
    return redirect(f'/posts/{pp}')
