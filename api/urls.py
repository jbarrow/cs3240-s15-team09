from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^authenticate/$', views.auth, name='authenticate'),
    url(r'^reports/$', views.get_reports, name='get_reports'),
    url(r'^files/(?P<report_id>[0-9]+)/$', views.get_file_list, name='get_file_list'),
    url(r'^download/(?P<file_id>[0-9]+)/$', views.get_file, name='get_file'),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.get_report, name='get_report'),
)
