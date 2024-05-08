from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Comment
from .forms import UserRegistrationForm, ProfileForm, PostForm, CommentForm
from django.utils.translation import gettext_lazy as _


@login_required
def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'blog/login.html', {'error': _('Nieprawidłowe dane logowania')})
    else:
        return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            raw_password = user_form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'blog/signup.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'blog/profile.html', {'profile': profile})

@login_required
def create_post(request):
    if not request.user.profile.role == Profile.Role.AUTHOR:
        return HttpResponseForbidden("Nie masz uprawnień do tworzenia postów.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    if not request.user == Post.objects.get(pk=post_id).author:
        return HttpResponseForbidden("Nie masz uprawnień do edycji tego wpisu.")

    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    if not request.user == Post.objects.get(pk=post_id).author:
        return HttpResponseForbidden("Nie masz uprawnień do usunięcia tego wpisu.")
    
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})
