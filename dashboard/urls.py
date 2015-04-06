from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('', 
url(r'^profile/$', views.user_profile),
)
