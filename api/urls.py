from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^authenticate/$', views.auth, name='authenticate'),
    url(r'^reports/$', views.get_reports, name='get_reports'),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.get_report, name='get_report'),
)
