import json
import os
import urllib
import urllib2

from PIL import Image
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from blog.token_generator import account_activation_token
from .models import Post, Profile, Comment
from django.utils import timezone
from .forms import PostForm, SignupForm, ProfileForm, CommentForm
from django.core.mail import send_mail
from .forms import EmailPostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).filter(draft=False).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('created_date')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_date = timezone.now()
            comment.approved = True
            comment.save()
            form = CommentForm()
            return render(request, 'blog/post_detail.html',
                          {'post': post, 'post_author': str(post.author), 'request_user': str(request.user),
                           'comments': comments, 'comment_form': form})

    else:
        form = CommentForm()
        return render(request, 'blog/post_detail.html',
                      {'post': post, 'post_author': str(post.author), 'request_user': str(request.user),
                       'comments': comments, 'comment_form': form})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            if "draft_button" in form.data:
                # save as draft
                post.draft = True
            else:
                post.draft = False
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {'form': form, "post_image_from_view": None})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            if "draft_button" in form.data:
                # save as draft
                post.draft = True
            else:
                post.draft = False
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post_image_from_view': post.post_image})


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
            send_mail(subject, message, 'thelixirblog@gmail.com', [cd['to']])
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
        if form.is_valid() and recaptcha_status(request):
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.is_active = False
            user.save()

            # Sending email with token to user
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message = ("Hi {}, Please click on the link to confirm your registration, \
                       http://{}/activate/{}/{}").format(user.username, current_site.domain, uid, token)

            send_mail("Activate your Elixir Account!", message, 'thelixirblog@gmail.com', [user.email])

            # Redirect user to page where they see email verification has been sent
            return render(request, 'blog/email_verification.html', {})
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

    return render(request, 'blog/profile_update.html',
                  {'form': form, 'profile_picture': request.user.profile.profile_picture})


@login_required()
def profile_detail(request):
    form = ProfileForm(request.POST, request.FILES)
    return render(request, 'blog/profile_detail.html', {'form': form})


@login_required()
def welcome(request):
    return render(request, 'blog/welcome_page.html', {})


def email_verification(request):
    # TODO send email
    return render(request, 'blog/email_verification.html', {})


def activate_account(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('welcome')


def recaptcha_status(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = json.load(response)

    if result['success']:
        return True
    return False
