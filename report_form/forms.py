from django import forms
from report_form.models import Folder
from django.forms import ModelForm

AUTHOR = 1
SHORT_DESC = 2
LOCATION = 3
DETAILED_DESC = 4
DOI = 5
PRIVATE = 6
KEYWORD = 7

SEARCH_CHOICES = (
    (AUTHOR, 'User ID'),
    (SHORT_DESC, 'Short Description'),
    (LOCATION, 'Location'),
    (DETAILED_DESC, 'Detailed Description'),
    (DOI, "Date of Incident"),
    (PRIVATE, "Private"),
    (KEYWORD, "Keyword"),
    )


class report_input_form(forms.Form):
    short_description = forms.CharField(label="Short Description: ", max_length=750)
    location = forms.CharField(label="Location of Incident: ", max_length=500, required=False)
    detailed_description = forms.CharField(label="Detailed Description: ", widget=forms.Textarea)
    date_of_incident = forms.DateTimeField(label="Date of Incident: ", required=False,
                                           input_formats=['%m/%d/%Y', '%m/%d/%y'])
    private = forms.BooleanField(label="Private: ", required=False)


class new_folder_form(ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class search_query(forms.Form):
    search_input = forms.CharField(label="Enter a search string ")
    category = forms.ChoiceField(label ="Search Category", choices = SEARCH_CHOICES)
