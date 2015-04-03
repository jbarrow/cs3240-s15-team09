from django.conf.urls import patterns, url
from group_form import views

urlpatterns = patterns('', 
url(r'^add-a-member/$', views.add_user, name='add_user'),
)
