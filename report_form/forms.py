from django import forms
from report_form.models import Folder


class report_input_form(forms.Form):
    # author = forms.CharField(label= 'Username: ', max_length=128)
    short_description = forms.CharField(label="Short Description: ", max_length=750)
    location = forms.CharField(label="Location of Incident: ", max_length=500, required=False)
    detailed_description = forms.CharField(label="Detailed Description: ", widget=forms.Textarea)
    date_of_incident = forms.DateTimeField(label="Date of Incident: ", required=False,
                                           input_formats=['%m/%d/%Y', '%m/%d/%y'])
    private = forms.BooleanField(label="Private: ", required=False)


class new_folder_form(forms.ModelForm):
    class Meta:
        model = Folder
        fields = {'name', }