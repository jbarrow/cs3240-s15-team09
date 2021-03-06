from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'secure_witness.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'secure_witness.views.register'),
    url(r'^accounts/admin/$', 'secure_witness.views.admin_test'),
    url(r'^accounts/profile/$', 'secure_witness.views.profile'),
    url(r'^report_form/', include('report_form.urls', namespace="report_form")),
    url(r'^groups/', include('group_form.urls', namespace="groups")),
    url(r'^swadmin/', include('swadmin.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^$', RedirectView.as_view(url='accounts/profile')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
