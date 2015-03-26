from django.conf.urls import patterns, url
from report_form import views

urlpatterns = patterns('', 
url(r'^make-a-report/$', views.submission, name='submission'),
url(r'^in-dev/$', views.incomplete_landing, name='incomplete_landing'),
url(r'^submitted/$', views.submitted, name='submitted'),)
