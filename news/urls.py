from django.urls import path
from .views import PostList, PostDateil, PostSearch

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDateil.as_view()),
    path('search/', PostSearch.as_view()),
]
