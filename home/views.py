from tkinter import E
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.core.paginator import Paginator
from home.models import Category, Post, Comment, Subscribe
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import PostCommentForm, SignUpForm
from django.contrib import auth

# Create your views here.


def index(request):
    return render(request, 'index.html')


def posts(request):
    if "category" in request.GET:
        category_data = Category.objects.get(slug=request.GET['category'])
        posts = Post.objects.all().filter(category=category_data)
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()[:3]
    latest_posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'posts.html', {'page_obj': page_obj, 'categories': categories, 'latest_posts': latest_posts})


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    tags = post.tags.all()
    comments = Comment.objects.all().filter(post=post).filter(parent=None)
    categories = Category.objects.all()[:3]
    all_comments = Comment.objects.all().filter(post=post).count()
    latest_posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'post_detail.html', {'post': post, 'tags': tags, 'categories': categories, 'comments': comments, 'all_comments': all_comments, 'latest_posts': latest_posts})


def post_comment(request):
    try:
        form = PostCommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk=request.POST['post_id'])
            if 'parent_id' in request.POST:
                parentComment = Comment.objects.get(
                    pk=request.POST['parent_id'])
                comment = Comment(
                    user_comment=request.POST['user_comment'], post=post, user=request.user, parent=parentComment)
            else:
                comment = Comment(
                    user_comment=request.POST['user_comment'], post=post, user=request.user)
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request, 'Please enter comment')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        raise e


def categories(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    latest_posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'categories.html', {'page_obj': page_obj, 'latest_posts': latest_posts})


def subscribe(request):
    try:
        email = request.POST['email']
        subscribe = Subscribe.objects.create(email=email)
        subscribe.save()
        messages.success(request, 'Subscribed successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        raise e


@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def login(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(request.GET.get('next', 'index'))
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')
        except Exception as e:
            raise e
    return render(request, 'auth/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')
    return HttpResponse("Invalid Request")


@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def register(request):
    if request.method == 'POST':
        try:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username,
                                    password=raw_password)
                auth_login(request, user)
                # redirect user to home page
                return redirect('index')
            return render(request, 'auth/register.html', {'form': form})
        except Exception as e:
            raise e
    return render(request, 'auth/register.html')
