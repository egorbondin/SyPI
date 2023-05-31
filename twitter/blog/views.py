from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import *
from .forms import PostForm, CreateUserForm
from .models import Like

@login_required(login_url='login')
def unconfirmed_posts(request):
    posts = UnconfirmedPost.objects.all()
    context = _get_role_context(request)
    context['posts'] = posts
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if 'accept' in request.POST:
            u_post = UnconfirmedPost.objects.get(pk=post_id)
            new_post = Post(author=u_post.author, title=u_post.title, content=u_post.content, post_type='group')
            new_post.save()
            u_post.delete()
        elif 'deny' in request.POST:
            UnconfirmedPost.objects.get(pk=post_id).delete()
        return redirect('unconfirmed_posts')
    return render(request, 'blog/uncomfirmedposts.html', context=context)


@login_required(login_url='login')
def suggest_post(request):
    context = _get_role_context(request)
    if request.method == 'POST':
        return _suggest_post(request)
    return render(request, 'blog/suggestpost.html', context=context)

@require_POST
def toggle_like(request):
    post_id = request.POST.get('post_id')
    response_data = {}

    if post_id:
        post = Post.objects.get(pk=post_id)
        user = request.user

        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            response_data['liked'] = False
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user)
            response_data['liked'] = True

        response_data['likes_count'] = post.get_likes_count

    return JsonResponse(response_data)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            messages.info(request, 'Неправильный логин/пароль')

    data = {}
    return render(request, 'blog/login.html', context=data)


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect('login')


def sign_up_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    data = {'form': form}
    return render(request, 'blog/signup.html', context=data)


@login_required(login_url="login")
def user_page(request, pk):
    user = request.user
    posts = Post.objects.filter(author=User.objects.get(pk=pk)) 
    context = _get_role_context(request)
    context['posts'] = posts
    context['mypage'] = User.objects.get(pk=pk) == user
    all_subs = user.followed_blogs.all()
    followed_users = []
    for sub in all_subs:
        if sub.follower == user and sub.followed_blog not in followed_users:
            followed_users.append(sub.followed_blog)
    context['followed'] = User.objects.get(pk=pk) in followed_users
    context['userpage_user'] = User.objects.get(pk=pk)

    if request.method == 'POST':
        if context['followed'] is False:
            new_sub = Subscription(follower=request.user, followed_blog=User.objects.get(pk=pk))
            new_sub.save()
        else:
            print('PADPISKA EST')
            old_sub = Subscription.objects.get(follower=request.user, followed_blog=User.objects.get(pk=pk))
            old_sub.delete()
        return redirect('user_page', pk)


    return render(request, 'blog/userpage.html', context=context)


@login_required(login_url="login")
def feed(request):
    user = request.user
    posts_for_user = []
    all_subs = user.followed_blogs.all()
    followed_users = []
    for sub in all_subs:
        if sub.follower == user and sub.followed_blog not in followed_users:
            followed_users.append(sub.followed_blog)
    
    all_posts = Post.objects.all()
    for post in all_posts:
        if post.author in followed_users or post.post_type == 'admin' \
                    or post.author == user \
                    or ((post.post_type == 'group' or post.post_type == 'teacher' ) and _get_role_context(request)['isStudent']) \
                    or ((post.post_type == 'group' or post.post_type == 'teacher' ) and _get_role_context(request)['isElder']):
            posts_for_user.append(post)
    context = _get_role_context(request)
    context['posts'] = posts_for_user
    return render(request, 'blog/feed.html', context=context)


@login_required(login_url="login")
def single_post(request, pk):
    post = Post.objects.get(pk=pk)
    context = _get_role_context(request)
    context['post'] = post

    if request.method == 'POST':
        post.delete()
        return redirect('feed')

    return render(request, 'blog/post.html', context=context)


@login_required(login_url="login")
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = Post.objects.get(id=post_id)
        Comment.objects.create(content=content, author=request.user, post=post)
    return redirect('single_post', post_id)


@login_required(login_url="login")
def create_group_post(request):
    post_type = 'Групповой'
    if request.method == 'POST':
        return _send_post_base(request, post_type)
    else:
        form = PostForm()
        context = _get_role_context(request)
        context['form'] = form
        context['type'] = post_type
        return render(request, 'blog/newpost.html', context=context)


@login_required(login_url="login")
def create_teacher_post(request):
    post_type = 'Преподавательский'
    if request.method == 'POST':
        return _send_post_base(request, post_type) 
    else:
        form = PostForm()
        context = _get_role_context(request)
        context['form'] = form
        context['type'] = post_type
        return render(request, 'blog/newpost.html', context=context)


@login_required(login_url="login")
def create_admin_post(request):
    post_type = 'Административный'
    if request.method == 'POST':
        return _send_post_base(request, post_type) 
    else:
        form = PostForm()
        context = _get_role_context(request)
        context['form'] = form
        context['type'] = post_type
        return render(request, 'blog/newpost.html', context=context)


@login_required(login_url="login")
def create_personal_post(request):
    post_type = 'Личный'
    if request.method == 'POST':
        return _send_post_base(request, post_type) 
    else:
        form = PostForm()
        context = _get_role_context(request)
        context['form'] = form
        context['type'] = post_type
        return render(request, 'blog/newpost.html', context=context)


@login_required(login_url="login")
def search_page(request):
    context = _get_role_context(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        users = User.objects.all()
        users_found = []
        for user in users:
            if (user.first_name.lower() == name.lower() \
            or user.last_name.lower() == name.lower() \
            or user.username.lower() == name.lower()) and (user not in users_found):
                users_found.append(user)
        context['users'] = users_found
    return render(request, 'blog/search.html', context=context)



def _suggest_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    s_post = UnconfirmedPost(title=title, content=content, author=request.user)
    s_post.save()
    return redirect('feed')

def _send_post_base(request, post_type):
    types = {
        'Административный': 'admin',
        'Личный': 'personal',
        'Преподавательский': 'teacher',
        'Групповой': 'group'
    }
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.post_type = types[post_type]
        post.save()
        return redirect('single_post', pk=post.pk)


def _get_role_context(request):
    user = request.user
    groups = user.groups.all()
    context = {
        'isAdmin': groups.filter(name='university_admins').exists(),
        'isTeacher': groups.filter(name='teachers').exists(),
        'isElder': groups.filter(name='elders').exists(),
        'isStudent': groups.filter(name='students').exists(),
        'user_pk': user.pk,
        'user' : user
    }
    return context