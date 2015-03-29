from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from secure_witness.models import UserProfile
from group_form.models import Group
from group_form.forms import add_user_group_form

def submitted(request):
	# want to echo back form fields here for confirmation
    return render(request, 'group_form/submission_template.html', {'submission' : submission})


def submission(request):
    return render(request, 'group_form/submission_template.html', {'submission' : submission})
