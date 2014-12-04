from django.conf.urls import patterns, url
from real_fantasy_adventure_app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        )