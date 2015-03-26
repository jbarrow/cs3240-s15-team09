from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from report_form.models import Report, User, File, FileForm, ReportForm

def incomplete_landing(request):
	return HttpResponse("Report form not yet available.")

def submitted(request):
	# want to echo back form fields here for confirmation
	return HttpResponse("Thank you!")

def submission(request):
	if request.method == 'POST':
		input_report_form = ReportForm(request.POST)
		input_file_form = FileForm(request.POST, request.FILES)
		if input_report_form.is_valid(): # change this
			# need to do the linking here
			# need to figure out how to do the multiple files
			# figure out how to do required/nonrequired fields with model forms
			# though we could append two forms together, though that is not great
			#for upfile in request.FILES.getlist("file"):
				#newfile = File(title = upfile.name, file=upfile)
				#newfile.save()

			return HttpResponseRedirect(reverse('report_form.views.submitted'))
	else:
		input_report_form = ReportForm()
		input_file_form = FileForm()

	return render(request, 'report_form/report_form_template.html', {'input_file_form' : input_file_form, 'input_report_form' : input_report_form})