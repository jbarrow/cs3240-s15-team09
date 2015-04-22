from django import forms
from report_form.models import Folder
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget

AUTHOR = 1
SHORT_DESC = 2
LOCATION = 3
DETAILED_DESC = 4
KEYWORD = 5

SEARCH_CHOICES = (
    (AUTHOR, 'User ID'),
    (SHORT_DESC, 'Short Description'),
    (LOCATION, 'Location'),
    (DETAILED_DESC, 'Detailed Description'),
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

class multi_cat_search_query(forms.Form):
    search_input = forms.CharField(label="Enter a search string ")
    category = forms.MultipleChoiceField(label ="Search Category", widget=forms.CheckboxSelectMultiple, choices = SEARCH_CHOICES)

class single_search_query(forms.Form):
    search_input = forms.CharField(label="Enter a search string ")
    category = forms.ChoiceField(label ="Search Category", choices = SEARCH_CHOICES)

class multi_field_multi_cat_search(forms.Form):
    s_author = forms.CharField(label="Username ", required=False)
    s_short_desc = forms.CharField(label="Short Description ", required=False)
    s_location = forms.CharField(label="Location ", required=False)
    s_detailed_desc = forms.CharField(label="Detailed Description ", required=False)
    s_keyword = forms.CharField(label="Keyword ", required=False)
    s_date = forms.DateTimeField(label= "Date of Incident ", widget=SelectDateWidget, required=False)

class folder_select(ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.filter())

