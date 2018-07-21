from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Profile
from django.utils import timezone
from .forms import PostForm, SignupForm, ProfileForm
from django.core.mail import send_mail
from .forms import EmailPostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',
                  {'post': post, 'post_author': str(post.author), 'request_user': str(request.user)})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_share(request, pk):
    # Retrieve post by id
    post = get_object_or_404(Post, pk=pk)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'anshumansblog@mail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post_share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def about_admins(request):
    context = {}
    return render(request, 'blog/about_admins.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'blog/logout.html', {})
    else:
        return render(request, 'blog/logout.html', {})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return render(request, 'blog/post_delete.html')
    else:
        post.delete()
    return render(request, 'blog/post_delete.html')


@login_required()
def user_specific_post_list(request):
    posts = Post.objects.filter(author=request.user)
    # if no posts, add post redirect
    return render(request, 'blog/post_list_user.html', {'posts': posts})


@login_required()
def profile_update(request):
    try:
        profile = request.user.profile
    except Exception:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=False)
            profile = form
            print(request.user.profile.profile_picture)
            profile.save()
            print(request.user.profile.profile_picture)
            return render(request, 'blog/profile_detail.html', {'form': form})
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/profile_update.html', {'form': form})


@login_required()
def profile_detail(request):
    form = ProfileForm(request.POST, request.FILES)
    return render(request, 'blog/profile_detail.html', {'form': form})
