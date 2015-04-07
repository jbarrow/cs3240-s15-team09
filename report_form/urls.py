from django.conf.urls import patterns, url
from report_form import views

urlpatterns = patterns('', 
url(r'^make-a-report/$', views.submission, name='submission'),
url(r'^in-dev/$', views.incomplete_landing, name='incomplete_landing'),
url(r'^submitted/$', views.submitted, name='submitted'),
url(r'^my-reports/(?P<user_id>[0-9]+)/$', views.my_reports, name='my_reports'),
url(r'^view-report/(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
url(r'^edit-report/(?P<report_id>[0-9]+)/$', views.edit, name='edit'),
url(r'^download/$', views.download, name='download'),)
