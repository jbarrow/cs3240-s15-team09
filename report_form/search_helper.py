from report_form.models import Report, Tag
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from datetime import date

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

def non_hierarchical_parsing(query):
	# DON'T PAY ATTENTION TO ANY OF THIS...
	q_set = []
	ands = string_parse(" AND ", query)
	ors = string_parse(" OR ", query)
	if len(ands) == 0 and len(ors) == 0:
		q_set.append(query)
	elif len(ands) > len(ors):
		ors = []
		for term in ands:
			y = string_parse(" OR ", term)
			if len(y) != 0:
				for x in y:
					ors.append(x)
	else:
		ands = []
		for term in ors:
			y = string_parse(" AND ", term)
			if len(y) != 0:
				for x in y:
					ands.append(x)
	print(ors)
	print(ands)
	print(q_set)

#non_hierarchical_parsing("this AND that AND else OR if")

# right now, I only can do AND XOR OR searches, and then multicategory searches, but not more
# still need to implement advanced searches

def advanced_query(query_list): # this does an implicit intersection
	collection = []
	nonempty = []
	author_set =[]
	short_desc_set = []
	location_set = []
	detailed_set = []
	kword_set = []
	date_set = []
	if query_list[0] != '': # author
		author_set = simple_return(AUTHOR, query_list[0])
	if query_list[1] != '': # short desc
		short_desc_set = simple_return(SHORT_DESC, query_list[1])
	if query_list[2] != '': # location
		location_set = simple_return(LOCATION, query_list[2])
	if query_list[3] != '': # detailed desc
		detailed_set = simple_return(DETAILED_DESC, query_list[3])
	if query_list[4] != '': # keyword
		kword_set = simple_return(KEYWORD, query_list[4])
	if query_list[5] != '0' and query_list[6] != '0' and query_list[7] != '0' : # date, could make this field searchable, but right now it is not
		DOI = date(day= int(query_list[7]), month=int(query_list[6]), year=int(query_list[5]))
		date_set = Report.objects.filter(date_of_incident=DOI)

	collection.append(author_set)
	collection.append(short_desc_set)
	collection.append(location_set)
	collection.append(detailed_set)
	collection.append(kword_set)
	collection.append(date_set)

	for simple in collection:
		if len(simple) != 0:
			nonempty.append(simple)

	retSet = set()
	if len(nonempty) > 0:
		retSet = nonempty[0]
		for x in nonempty:
			retSet = set.intersection(set(retSet), set(x)) 

	return retSet

def multi_cat_return_OR(categories, search_strings):
	retSet = []
	print(search_strings)
	for cat in categories:
		for query in search_strings:
			retSet = set.union(set(retSet), set(simple_return(cat, query)))
	return retSet