from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^authenticate/$', views.auth, name='authenticate'),
    url(r'^reports/$', views.get_reports, name='get_reports'),
)
