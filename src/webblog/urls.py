from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from sitemaps import indexSitemap
from blog.views import Home, CategoryView, TagView, PostView

sitemaps = {
    'main': indexSitemap,
}

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    
    # Yandex access
    url(r'yandex_4176ffddb576e745.html$', 'webblog.views.yandex_access'),
    # robot.txt
    url(r'robots\.txt', 'webblog.views.robots'),


    url(r'^$', Home.as_view(), name='home'),
    url(r'^category/(?P<category>[_a-zA-Z0-9]+)/$', CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag>[_a-zA-Z0-9]+)/$', TagView.as_view(), name='tag'),
    url(r'^post/(?P<post>[_a-zA-Z0-9/-]+)/$', PostView.as_view(), name='post'),
    # url(r'^webblog/', include('webblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


)

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ) + urlpatterns
