from django import forms
from group_form.models import Group
from django.contrib.auth.models import User

class add_user_group_form(forms.Form):
    user = forms.CharField(label="Username of User to Add")
    group = forms.ChoiceField(label="Group to add them to")
    def __init__(self, user, *args, **kwargs):
        super(add_user_group_form, self).__init__(*args, **kwargs)
        if isinstance(user, User):
            if user.is_swadmin:
                self.fields['group'] = forms.ChoiceField(choices=[(o.id, str(o)) for o in Group.objects.all()])
            else:
                self.fields['group'] = forms.ChoiceField(choices=[(o.id, str(o)) for o in Group.objects.filter(users=user)])



