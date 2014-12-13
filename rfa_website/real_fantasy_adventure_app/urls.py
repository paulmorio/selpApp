from django.conf.urls import patterns, url
from real_fantasy_adventure_app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^avatar/(?P<avatar_name_slug>[\w\-]+)/$', views.avatarProfile, name='avatar'),
        url(r'^avatar/(?P<avatar_name_slug>\w+)/add_myQuest/$', views.add_myQuest, name='add_myQuest'),
    	url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        )