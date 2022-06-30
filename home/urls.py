from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.posts, name='posts'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('categories', views.categories, name='categories'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('post-comment', views.post_comment, name='post_comment'),
    path('subscribe', views.subscribe, name='subscribe')
]
