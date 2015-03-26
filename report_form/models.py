from django.db import models
from django.forms import ModelForm


class Group(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name



class Report(models.Model):

    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    location = models.CharField(max_length=500)
    time = models.DateTimeField()
    #time_created = models.DateTimeField.auto_now_add();
    #time_last_modified = models.DateTimeField.auto_now();


    def __str__(self):
        return self.title

class File(models.Model):
    title = models.CharField(max_length=128, unique=True)
    file = models.FileField()
    report = models.ForeignKey(Report)

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['author', 'title', 'location', 'time']

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

# class InputForm(models.Model):
# 	name = models.CharField(label = 'Username:', max_length=100)
# 	location = models.CharField(label = 'Location of Incident:', max_length=500, required=False)
# 	time = models.DateTimeField(label = 'Time of Incident:', required=False, input_formats = ['%m/%d/%Y', '%m/%d/%y'], help_text='format is like: 12/20/2014')
# 	desc = models.CharField(label= 'Incident Description:', widget=forms.Textarea)
# 	privacy = models.BooleanField(label = 'Is this a private report?')
# 	alt_privacy = models.ChoiceField(label = 'Select privacy setting', choices=(('Private', 'PRIVATE'), ('Public','PUBLIC'),), required=False)
# 	input = models.FileField(label = 'Select a file to upload')
# 	next_one = models.FileField(label = 'input a second file')
