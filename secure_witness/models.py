from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.username