from report_form.models import Report, Tag
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
AUTHOR = '1'
SHORT_DESC = '2'
LOCATION = '3'
DETAILED_DESC = '4'
DOI = '5'
PRIVATE = '6'
KEYWORD = '7'

def simple_return(category, search_string):
	# only for public reports
	retSet = []
	if category == AUTHOR:
		users = User.objects.filter(username=search_string)
		if len(users) > 0:
			profile = UserProfile.objects.filter(user=users[0])
			if len(profile) > 0:
				return Report.objects.filter(author=profile[0], private=False)
			else:
				return retSet
		else:
			return retSet
	elif category == SHORT_DESC:
		return Report.objects.filter(short_description=search_string)
	elif category == LOCATION:
		return Report.objects.filter(location=search_string)
	elif category == DETAILED_DESC:
		return Report.objects.filter(detailed_description=search_string)
	elif category == DOI:
		# more difficult
		return retSet
	elif category == KEYWORD:
		# make private -- this would be more difficult
		all_keywords = Tag.objects.filter(keyword=search_string)
		for kword in all_keywords:
			keywordSet = []
			keywordSet.append(kword.associated_report)
			for report in keywordSet:
				if not report.private:
					retSet.append(report)
		return retSet
	else:
		return retSet

