from django import forms

class add_user_group_form(forms.Form):
	user = forms.CharField(label= 'Username of User to Add: ', max_length=128)
	group = forms.CharField(label= "Group to add them to: ", max_length=128)
