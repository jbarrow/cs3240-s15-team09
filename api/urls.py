from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^authenticate/$', views.auth, name='authenticate'),
)
