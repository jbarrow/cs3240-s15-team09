from django import template
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from report_form.models import Permission, Report, Tag, File
from django.shortcuts import render, get_object_or_404
from group_form.models import Group
from report_form.filter_helper import get_shared_reports

register = template.Library()


@register.filter(name='filter_by_permissions')
def filter_by_permissions(results):
    # this will get a set of reports
    # this will return a set of reports
    # the last value of the results object will be the user for now
    # remove the current user and continue
    results = list(results)
    profile = results.pop()  # will remove and return the last item in the list
    retSet = set()
    for report in results:
        if not report.private or profile.profile.admin:
            retSet.add(report)
        else:
            p = get_object_or_404(Permission, report=report)
            if profile.profile in p.profiles.all() or profile.profile == report.author:
                retSet.add(report)
            for g in p.groups.all():
                if profile in g.users.all():
                    retSet.add(report)
    return retSet


