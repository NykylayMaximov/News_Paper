from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Функция перебирает полученный QuerySet, добавляет значение рейтинга на новый список и возвращает сумму списка
def rating_list_sum(rating_queryset):
    rating_list = []
    for i in list(rating_queryset):
        rating_list.append(i['rating'])
    return sum(rating_list)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0
        posts_rating = Post.objects.filter(author=self).values('rating')
        posts_rating_sum = rating_list_sum(posts_rating)

        posts_comments_rating = Comment.objects.filter(post__author=self).values('rating')
        posts_comments_rating_sum = rating_list_sum(posts_comments_rating)

        comments_rating = Comment.objects.filter(user__id=self.user_id).values('rating')
        comments_rating_sum = rating_list_sum(comments_rating)

        self.rating = posts_rating_sum * 3 + posts_comments_rating_sum + comments_rating_sum
        self.save()

    # def __str__(self):
    #     return self.user


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, through='SubscribeCategory', related_name='subscribers')

    def __str__(self):
        return self.category


class SubscribeCategory(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_or_news = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."

    def __str__(self):
        return f'{self.title}: {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

