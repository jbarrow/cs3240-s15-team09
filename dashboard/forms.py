from django import forms
from secure_witness.models import UserProfile

class user_profile_form(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('name',)
