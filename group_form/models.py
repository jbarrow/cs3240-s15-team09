from django.db import models
from django.contrib.auth.models import User
#from secure_witness.models import UserProfile
#from report_form.models import Permission

class Group(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField('secure_witness.UserProfile')
    permissions = models.ManyToManyField('report_form.Permission')


    def __str__(self):
        return self.name
