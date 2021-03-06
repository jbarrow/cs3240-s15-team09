from django.conf.urls import patterns, url
from swadmin import views

urlpatterns = patterns('',
    url(r'^users/$', views.view_users, name='users'),
    url(r'^users/makeadmin/(?P<user_id>[0-9]+)$', views.make_admin, name='users'),
    url(r'^users/suspend/(?P<user_id>[0-9]+)$', views.suspend, name='users'),
    url(r'^users/unsuspend/(?P<user_id>[0-9]+)$', views.unsuspend, name='users'),
    url(r'^groups/$', views.view_groups, name='groups'),
    url(r'^groups/create/$', views.create_group, name='create_group'),
    url(r'^groups/delete/(?P<group_id>[0-9]+)$', views.delete_group, name='delete_group'),
    url(r'^groups/edit/(?P<group_id>[0-9]+)$', views.edit_group, name='edit_group'),
    url(r'^reports/$', views.view_all_reports, name='view_all_reports'),
)
