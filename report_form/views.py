from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from report_form.models import Report, User, File, FileForm, ReportForm

def incomplete_landing(request):
	return HttpResponse("Report form not yet available.")

def submission(request):
	if request.method == 'POST':
		input_report_form = ReportForm(request.POST)
		input_file_form = FileForm(request.POST, request.FILES)
		if input_report_form.is_valid():
			return HttpResponseRedirect(reverse('report_form.views.submission'))
	else:
		input_report_form = ReportForm()
		input_file_form = FileForm()
		
	return render(request, 'report_form/report_form_template.html', {'input_file_form' : input_file_form, 'input_report_form' : input_report_form})
