from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'secure_witness.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # TODO: Add additional URLs

    url(r'^admin/', include(admin.site.urls)),
)
