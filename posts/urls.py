from django.urls import path
from posts import views
from .views import trending_posts

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/trending/', trending_posts, name='post-trending'),
]