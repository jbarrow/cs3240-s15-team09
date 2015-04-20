from django import template
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from report_form.models import Folder

register = template.Library()

@register.filter(name='retrieve_folders')
def retrieve_folders(value):
    userprofile = value
    folders = Folder.objects.filter(userprofile = userprofile)
    unsorted_folder = Folder.objects.get(userprofile=userprofile, name = "unsorted")
    folders = folders.exclude(pk=unsorted_folder.pk)
    return folders
