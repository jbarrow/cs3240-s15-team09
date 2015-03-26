from django.conf.urls import patterns, url
from report_form import views

urlpatterns = patterns('', 
#url(r'^report_submission/$', views.incomplete_landing, name='incomplete_landing'),
url(r'^$', views.incomplete_landing, name='incomplete_landing'),)
