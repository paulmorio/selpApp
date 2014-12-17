from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rfa_website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Enables Admin
    url(r'^admin/', include(admin.site.urls)),

    # Enables Markdown inclusion in the admin page, used for dev_blog app 
    # (if time permits after rfa is complete)
    url(r'^markdown/', include("django_markdown.urls")),

    # Let URL mapping of anything related to the rfa app be handled by urls.py in the app, this decouples
    # the mappings and makes it possible to move real_fantasy_adventure_app between projects.
    url(r'^real_fantasy_adventure_app/', include('real_fantasy_adventure_app.urls')),
)
