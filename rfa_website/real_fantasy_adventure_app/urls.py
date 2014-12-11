from django.conf.urls import patterns, url
from real_fantasy_adventure_app import views

urlpatterns = patterns('',
        url(r'^index', views.index, name='index'),
        url(r'^about', views.about, name='about'),
        url(r'^avatar/(?P<avatar_name_slug>[\w\-]+)/$', views.avatarProfile, name='avatar'),
        )