from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<pk>\d+)/share/$', views.post_share, name='post_share'),
	url(r'^about_admins/$', views.about_admins, name ='about_admins'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^login/$', auth_views.login, {'template_name': 'blog/login.html'}, name='login')
]