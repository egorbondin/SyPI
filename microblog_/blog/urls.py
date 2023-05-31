from django.urls import path
from django.shortcuts import redirect
from .views import *

def redirect_to_feed(request):
    return redirect('feed')

urlpatterns = [
    path('', redirect_to_feed),
    path('feed/', feed, name='feed'),
    path('feed/<int:pk>/', single_post, name='single_post'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('create/mypost/', create_personal_post, name='create_personal'),
    path('create/grouppost/', create_group_post, name='create_group'),
    path('create/adminpost/', create_admin_post, name='create_admin'),
    path('create/teacherpost/', create_teacher_post, name='create_teacher'),
    path('search/', search_page, name='search'),
    path('user/<int:pk>', user_page, name='user_page'),
    path('login/', login_page, name='login'),
    path('signup/', sign_up_page, name='sign_up'),
    path('logout/', logout_user, name='logout'),
    path('toggle-like/', toggle_like, name='toggle_like'),
    path('suggestpost/', suggest_post, name='suggest_post'),
    path('unconfirmedposts/', unconfirmed_posts, name='unconfirmed_posts')
]

