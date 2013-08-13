from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache


admin.autodiscover()
urlpatterns = patterns('', )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', never_cache(serve_static)),
    )

urlpatterns += patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chart/', include('chordcharts.urls')),
)
