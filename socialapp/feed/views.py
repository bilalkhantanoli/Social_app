"""
This module contains the views for the feed app, handling user authentication,
post creation, and user profile management with HTMX support.
"""
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignupForm, CustomUserCreationForm, PostForm, CommentForm, ProfileForm
from .models import Post, Profile, Like, Comment
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'feed/home.html')

@login_required
def feed(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    form = PostForm()

    if request.headers.get('HX-Request') and request.GET.get('page'):
        return render(request, 'feed/partials/post_list.html', {'posts': posts})
    
    return render(request, 'feed/feed.html', {'posts': posts, 'form': form})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'feed/post.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    # Return partial for the like button/count
    return render(request, 'feed/partials/like_area.html', {'post': post})

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return render(request, 'feed/partials/comment.html', {'comment': comment})
    return HttpResponse(status=400)

@login_required
def profile(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user

    posts = Post.objects.filter(user=user_obj).order_by('-created_at')
    
    # Handle Profile Editing
    if request.user == user_obj:
        if request.method == 'POST':
            p_form = ProfileForm(request.POST, request.FILES, instance=user_obj.profile)
            if p_form.is_valid():
                p_form.save()
                return redirect('profile')
        else:
            p_form = ProfileForm(instance=user_obj.profile)
    else:
        p_form = None

    is_following = False
    if request.user != user_obj:
        if request.user.profile.following.filter(id=user_obj.profile.id).exists():
            is_following = True

    context = {
        'profile_user': user_obj,
        'posts': posts,
        'p_form': p_form,
        'is_following': is_following
    }
    return render(request, 'feed/profile.html', context)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile = request.user.profile
    target_profile = target_user.profile
    
    if user_profile.following.filter(id=target_profile.id).exists():
        user_profile.following.remove(target_profile)
        is_following = False
    else:
        user_profile.following.add(target_profile)
        is_following = True
        
    return render(request, 'feed/partials/follow_button.html', {
        'profile_user': target_user, 
        'is_following': is_following
    })

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("feed")
        else:
            return render(request, "feed/login.html", {"error": "Invalid credentials"})
    return render(request, "feed/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "feed/signup.html", {"form": form})

@login_required
def update_post(request, post_id):
    post_instance = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = PostForm(instance=post_instance)
    return render(request, 'feed/update_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post_instance = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        post_instance.delete()
        return redirect('feed')
    return render(request, 'feed/delete_post.html', {'post': post_instance})
