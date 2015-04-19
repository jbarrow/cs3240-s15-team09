from django import forms
from group_form.models import Group

class add_user_group_form(forms.Form):
	user = forms.CharField(label= "Username of User to Add")
	group = forms.ChoiceField(label= "Group to add them to")

