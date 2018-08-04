from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^about_admins/$', views.about_admins, name='about_admins'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'blog/logout.html'}, name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'blog/login.html'}, name='login'),
    url(r'^post/(?P<pk>\d+)/deleted/$', views.post_delete, name="post_delete"),
    url(r'^loggeduser/$', views.user_specific_post_list, name="user_specific_posts"),
    url(r'^profile_update/$', views.profile_update, name="profile_update"),
    url(r'^profile_detail/$', views.profile_detail, name="profile_detail"),
    url(r'^welcome_page/$', views.welcome, name="welcome"),



]
