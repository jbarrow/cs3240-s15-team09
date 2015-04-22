from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from group_form.models import Group
from report_form.models import Permission
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=128, null=True)
    session_token = models.CharField(max_length=255, null=True)
    groups = models.ManyToManyField('group_form.Group')
    admin = models.BooleanField(default=False)
    permissions = models.ManyToManyField('report_form.Permission')

    def generate_token(self):
        return uuid.uuid1().hex

    def __str__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get(user=u))
User.is_swadmin = property(lambda u: u.profile.admin)

def is_swadmin(u):
    return u.is_swadmin
