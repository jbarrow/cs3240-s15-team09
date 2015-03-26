from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from report_form.models import Report, User, File

def incomplete_landing(request):
	return HttpResponse("Report form not yet available.")

