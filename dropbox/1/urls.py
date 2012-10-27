from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^(?P<year>(?:\d{4}|\d{2}))/(?P<month>\d{1,2})/(?P<day>\d{1,2})$', eedition.views.show_edition)
)