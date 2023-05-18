from django.urls import path
from .views import PostList, PostDateil


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDateil.as_view()),
]