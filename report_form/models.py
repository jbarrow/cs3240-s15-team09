from django.db import models
from django.forms import ModelForm
from secure_witness.models import UserProfile
from Crypto.PublicKey import RSA

class Folder(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=128)
    #report = models.ForeignKey(Report)

    def __str__(self):
        return self.name


class Report(models.Model):

    author = models.ForeignKey(UserProfile)
    short_description = models.CharField(max_length=750)
    location = models.CharField(max_length=500, blank=True)
    detailed_description = models.TextField()
    date_of_incident = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    time_created = models.TimeField(auto_now_add = True);
    time_last_modified = models.DateTimeField(auto_now = True);
    #folder = models.ForeignKey(Folder, blank=True, initial=some value);

    def __str__(self):
        return self.short_description

class File(models.Model):
    title = models.CharField(max_length=128) #used to be unique = true... but I was having some errors
    file = models.FileField(upload_to='input/%Y/%m/%d')
    report = models.ForeignKey(Report)

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['short_description', 'detailed_description', 'location', 'date_of_incident','private']

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

# class InputForm(models.Model):
#   name = models.CharField(label = 'Username:', max_length=100)
#   location = models.CharField(label = 'Location of Incident:', max_length=500, required=False)
#   time = models.DateTimeField(label = 'Time of Incident:', required=False, input_formats = ['%m/%d/%Y', '%m/%d/%y'], help_text='format is like: 12/20/2014')
#   desc = models.CharField(label= 'Incident Description:', widget=forms.Textarea)
#   privacy = models.BooleanField(label = 'Is this a private report?')
#   alt_privacy = models.ChoiceField(label = 'Select privacy setting', choices=(('Private', 'PRIVATE'), ('Public','PUBLIC'),), required=False)
#   input = models.FileField(label = 'Select a file to upload')
#   next_one = models.FileField(label = 'input a second file')
