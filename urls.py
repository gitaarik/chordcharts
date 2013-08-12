from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve as serve_static
from django.views.decorators.cache import never_cache


admin.autodiscover()
urlpatterns = patterns('', )

if settings.DEBUG:

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', never_cache(serve_static), {
            'document_root': settings.STATIC_ROOT,
        }),
    )

urlpatterns += patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^chart/edit/'
         '(?P<song_slug>[a-z-_]*)/'
         '(?:(?P<key_slug>[a-z-_]*)/)?$',
        'chordcharts.views.chart',
        {'edit': True},
        name='chart_edit',
    ),
    url(
        r'^chart/'
         '(?P<song_slug>[a-z-_]*)/'
         '(?:(?P<key_slug>[a-z-_]*)/)?$',
        'chordcharts.views.chart',
        name='chart'
    ),
)
