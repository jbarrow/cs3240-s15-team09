from report_form.models import Report, Tag
from secure_witness.models import UserProfile
from django.contrib.auth.models import User

AUTHOR = '1'
SHORT_DESC = '2'
LOCATION = '3'
DETAILED_DESC = '4'
KEYWORD = '5'

def simple_return(category, search_string):
	# only for public reports
	retSet = []
	if category == AUTHOR:
		users = User.objects.filter(username=search_string)
		if len(users) > 0:
			profile = UserProfile.objects.filter(user=users[0])
			if len(profile) > 0:
				return Report.objects.filter(author=profile[0])
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
	elif category == KEYWORD:
		all_keywords = Tag.objects.filter(keyword=search_string)
		for kword in all_keywords:
			retSet.append(kword.associated_report)
		return retSet
	else:
		return retSet

# need to add set union and intersection for complex search queries
# also may want to have the ability to search multiple fields instead of just one


def multi_cat_return(categories, search_string):
	retSet = []
	for cat in categories:
		retSet = set.union(set(retSet), set(simple_return(cat, search_string)))
	return retSet

def string_parse(delimiter, search_string):
	search_string = search_string.strip()
	keywords = []
	index = 0
	prev_index = 0
	while search_string.find(delimiter, index) != -1:
		index = search_string.find(delimiter, prev_index)
		if index != -1:
			if prev_index == 0:
				term = search_string[prev_index: index]
			else:
				term = search_string[prev_index+len(delimiter)-1:index]
			prev_index = index+1
		else:
			term = search_string[prev_index+len(delimiter)-1:]
			prev_index = index+1
		keywords.append(term)
	return keywords