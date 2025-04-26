from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Profile, Post, Like, Comment  # Ensure all models are imported
from .forms import SignupForm, PostForm

# Profile View
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'instagram_clone/profile.html', {'user': user, 'posts': posts})

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to homepage after signup
    else:
        form = SignupForm()
    return render(request, 'instagram_clone/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'instagram_clone/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Create Post View
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'instagram_clone/create_post.html', {'form': form})

# Feed View
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'instagram_clone/feed.html', {'posts': posts})

# Like Post View (Fixed)
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()  # Unlike the post if already liked

    likes_count = Like.objects.filter(post=post).count()  # Correct way to count likes
    return JsonResponse({'likes_count': likes_count})

# Add Comment View
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        comment_text = request.POST.get('comment')
        Comment.objects.create(user=request.user, post=post, comment=comment_text)
        return redirect('feed')
