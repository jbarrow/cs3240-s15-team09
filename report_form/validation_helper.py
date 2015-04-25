from django.core.exceptions import ObjectDoesNotExist
from report_form.models import Permission, Report, Tag, File
from secure_witness.models import UserProfile
from django.contrib.auth.models import User

def permission_validation(user_name, perm_id):
	# input is a string that should be a user name
	# return is a boolean to indicate if operation could be done
	status = False
	try:
		user = User.objects.get(username=user_name)
		p = UserProfile.objects.get(user=user)
		perm = Permission.objects.get(id=perm_id)
		perm.profiles.add(p)
		status = True
	except ObjectDoesNotExist:
		status = False
	return status