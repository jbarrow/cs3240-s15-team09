from django.db import models
from django.forms import ModelForm
from secure_witness.models import UserProfile
from group_form.models import Group
from Crypto.PublicKey import RSA
from django.forms.extras.widgets import SelectDateWidget

class Folder(models.Model):
    name = models.CharField(max_length=128)
    userprofile = models.ForeignKey(UserProfile)


    def __str__(self):
        return self.name

class Report(models.Model):
    author = models.ForeignKey(UserProfile)
    short_description = models.CharField(max_length=750)
    location = models.CharField(max_length=500, blank=True)
    detailed_description = models.TextField()
    date_of_incident = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    #time_created = models.DateTimeField(auto_now_add = True);
    time_created = models.TimeField(auto_now_add = True);
    time_last_modified = models.DateTimeField(auto_now = True);
    folder = models.ForeignKey(Folder, blank=True, null=True);
    #groups = models.ForeignKey(Group, blank=True, null=True); # may be questionable because we may want a many to many relationship
    # or they could use the copy functionality in order to create lots of copies to share with other groups
    # how to make a report belong to multiple users?
    # don't actually allow this to be null, but we handle this on submission anyway

    def __str__(self):
        return self.short_description

class File(models.Model):
    title = models.CharField(max_length=128) #used to be unique = true... but I was having some errors
    file = models.FileField(upload_to='input/%Y/%m/%d')
    report = models.ForeignKey(Report)

class Tag(models.Model):
    keyword = models.CharField(max_length=128, null=True, blank=True)
    associated_report = models.ForeignKey(Report)

    def __str__(self):
        return self.name

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['short_description', 'detailed_description', 'location', 'date_of_incident', 'private', 'folder']
        widgets = {
        'date_of_incident' : SelectDateWidget,
        }
class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['keyword']