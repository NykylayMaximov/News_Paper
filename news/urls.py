from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDateil.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pp>/subscribe/<int:pk>', subscribe, name='subscribe'),
    path('<int:pp>/unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
]
