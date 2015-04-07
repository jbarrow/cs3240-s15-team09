from django.conf.urls import patterns, url
from swadmin import views

urlpatterns = patterns('',
    url(r'^users/$', views.view_users, name='users'),
)
