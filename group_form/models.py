from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
