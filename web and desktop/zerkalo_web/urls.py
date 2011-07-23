from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('editions.views',
    (r'^$', 'show'), # desktop
    (r'^m/$', 'show_m'), # advanced mobile
    (r'^m1/$', 'show_m1'), # old mobile
    
    (r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', 'show'),
    (r'^m/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', 'show_m'),
    (r'^m1/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', 'show_m1'),
    
    (r'^search.html', 'search'),
    (r'^m/search.html', 'search_m')
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)