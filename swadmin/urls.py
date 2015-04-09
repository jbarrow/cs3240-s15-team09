from django.conf.urls import patterns, url
from swadmin import views

urlpatterns = patterns('',
    url(r'^users/$', views.view_users, name='users'),
    url(r'^users/makeadmin/(?P<user_id>[0-9]+)$', views.make_admin, name='users'),
    url(r'^users/suspend/(?P<user_id>[0-9]+)$', views.suspend, name='users'),
)
