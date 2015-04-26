from django import template
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from report_form.models import Report, Tag, Permission
from datetime import date, timedelta
from report_form.views import simple_return
from django.shortcuts import render, get_object_or_404
import re

register = template.Library()




@register.filter(name='similar_reports')
def return_most_similar_reports(user, report_id):
    report = Report.objects.get(id=report_id)
    current_user = user
    profile = user.profile
    all_reports = Report.objects.all()
    for report2 in all_reports:
        if profile == report2.author:
            all_reports = all_reports.exclude(pk=report2.pk)
        if report2.private and not profile.admin:
            p = get_object_or_404(Permission, report=report2)
            if profile not in p.profiles.all():
                all_reports = all_reports.exclude(pk=report2.pk)
            for g in p.groups.all():
                if profile not in g.users.all():
                    all_reports = all_reports.exclude(pk=report2.pk)
            if report2.id == report_id:
                all_reports = all_reports.exclude(pk=report2.pk)

    list = []
    sim_reports = all_reports
    similarity_threshold = 3
    date_threshold = 3
    same_username = all_reports.filter(author=report.author)
    same_location = Report.objects.none()
    if report.location != None:
        same_location = all_reports.filter(location = report.location)
    similar_date = []
    most_commmon_words = MOSTCOMMON

    for cur_report in all_reports:
        if cur_report.date_of_incident != None and report.date_of_incident != None:
            delta = report.date_of_incident - cur_report.date_of_incident
            if abs(delta.days) < date_threshold:
                similar_date.append(cur_report)

    same_keyword = []
    report_keywords = Tag.objects.filter(associated_report=report)
    for kword in report_keywords:
        all_keywords = Tag.objects.filter(keyword__icontains=kword.keyword)

        for kword2 in all_keywords:
            assoc_report = kword2.associated_report
            if assoc_report in all_reports:
                same_keyword.append(assoc_report)

    similar_description = Report.objects.none()

    unique_words = []
    short_des_words = re.sub(r'([^\s\w]|_)+', u'', report.short_description, flags=re.LOCALE).lower().split()
    short_des_words = short_des_words + re.sub(r'([^\s\w]|_)+', u'', report.detailed_description, flags=re.LOCALE).lower().split()

    for word in short_des_words:
        if "\'" not in word:
            if word not in most_commmon_words:
                unique_words.append(word)


    for word in unique_words:
        similar_description = similar_description | all_reports.filter(short_description__icontains=word)
        similar_description = similar_description | all_reports.filter(detailed_description__icontains=word)

    for cur_report in all_reports:
        similarity = 0
        if cur_report in same_username:
            similarity = similarity + .2
        if cur_report in same_location:
            similarity = similarity + 1
        if cur_report in similar_date:
            similarity = similarity + 1

        list.append((cur_report, similarity))

    for cur_report in same_keyword:
        similarity = 5
        inList = False
        for tup in list:
            if cur_report in tup:
                inList = True
                similarity += tup[1]
                list.remove(tup)
                list.append((cur_report, similarity))
        if not inList:
            list.append((cur_report, similarity))

    for cur_report in similar_description:
        similarity = .2
        inList = False
        for tup in list:
            if cur_report in tup:
                inList = True
                similarity += tup[1]
                list.remove(tup)
                list.append((cur_report, similarity))
        if not inList:
            list.append((cur_report, similarity))

    list = sorted(list,key=lambda x:(-x[1]))
    count = 0
    for tup in list:
        count = count + 1
        if tup[1] < similarity_threshold or count > 5:

            sim_reports = sim_reports.exclude(id=tup[0].id)

    return sim_reports


MOSTCOMMON = """the be and of a in to have it I that for you he with on do say this they at but we his from not by she or as what go their
can
who
get
if
would
her
all
my
make
about
know
will
up
one
time
there
year
so
think
when
which
them
some
me
people
take
out
into
just
see
him
your
come
could
now
than
like
other
how
then
its
our
two
more
these
want
way
look
first
also
new
because
day
use
no
man
find
here
thing
give
many
well
only
those
tell
very
even
"""



