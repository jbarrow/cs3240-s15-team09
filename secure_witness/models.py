from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=128)
    #groups = models.ManyToManyField('group_form.Group')
    #admin = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username
