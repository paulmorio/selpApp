from django.conf.urls import patterns, url
from real_fantasy_adventure_app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^notLoggedIn/$', views.notLoggedIn, name='notLoggedIn'),
        url(r'^avatar/(?P<avatar_name_slug>[\w\-]+)/$', views.avatarProfile, name='avatar'),
        url(r'^avatar/(?P<avatar_name_slug>\w+)/add_myQuest/$', views.add_myQuest, name='add_myQuest'),
        url(r'^avatar/(?P<avatar_name_slug>\w+)/statChange/$', views.statChange, name='statChange'),
    	url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),    
        )