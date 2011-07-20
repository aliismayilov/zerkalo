from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('editions.views',
    (r'^$', 'show'),
    (r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', 'show'),
    (r'^search.html', 'search')
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)