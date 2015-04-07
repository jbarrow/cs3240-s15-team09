from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from group_form.models import Group

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=128)
    groups = models.ManyToManyField('group_form.Group')
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get(user=u)[0])
User.is_swadmin = property(lambda u: u.profile.admin)

def is_swadmin(u):
    return u.is_swadmin
