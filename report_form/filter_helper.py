from django import template
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from report_form.models import Permission, Report, Tag, File
from django.shortcuts import render, get_object_or_404
from group_form.models import Group


def filter_by_permissions(results, user):
	retSet = set()
	for report in results:
		if not report.private or user.profile.admin:
			retSet.add(report)
		else:
			# every report should have some sort of permission attached to it
			p = get_object_or_404(Permission, report=report)
			if user.profile in p.profiles.all() or user.profile == report.author:
				retSet.add(report)
			for g in p.groups.all():
				if user.profile in g.users.all():
					retSet.add(report)
	return retSet

def get_shared_reports(results, user):
	reports = filter_by_permissions(results, user)
	retSet = set()
	for r in reports:
		if r.author != user.profile:
			retSet.add(r)
	return retSet

def get_5_latest(results, user):
	# i'm assuming that the reports are filtered by id, so if we can find the 5 greatest ids
	# then we have the 5 latest
	reports = get_shared_reports(results, user)
	if len(reports) <= 5:
		return reports
	else:
		retSet = sorted(reports, key=lambda  Report:Report.id, reverse=True)
		retSet = retSet[:5]
		return retSet

