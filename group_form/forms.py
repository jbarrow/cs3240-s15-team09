from django import forms

class add_user_group_form(forms.Form):
	user = forms.CharField(label= "Username of User to Add")
	group = forms.ChoiceField(label= "Group to add them to")

