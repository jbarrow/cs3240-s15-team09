from django.conf.urls import patterns, url
from report_form import views

urlpatterns = patterns('',
url(r'^make-a-report/$', views.submission, name='submission'),
url(r'^in-dev/$', views.incomplete_landing, name='incomplete_landing'),
url(r'^submitted/$', views.submitted, name='submitted'),
url(r'^my-reports/(?P<user_id>[0-9]+)/$', views.my_reports, name='my_reports'),
url(r'^view-report/(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
url(r'^edit-report/(?P<report_id>[0-9]+)/$', views.edit, name='edit'),
url(r'^download/(?P<file_id>[0-9]+)/$', views.download, name='download'),
url(r'^simple-search/$', views.simple_search, name='simple_search'),
url(r'^advanced-search/$', views.advanced_search, name='advanced_search'),
url(r'^search-with-OR/$', views.search_with_OR, name='search_with_OR'),
)
