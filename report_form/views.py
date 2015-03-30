from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from report_form.models import Report, File
from report_form.forms import report_input_form
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def incomplete_landing(request):
	return HttpResponse("Report form not yet available.")

def submitted(request):
	# want to echo back form fields here for confirmation
	submission = Report.objects.latest('id')
	last_id = submission.id
	files = File.objects.filter(report=submission)
	#return HttpResponse("Thanks.")
	return render(request, 'report_form/submission_template.html', {'submission' : submission, 'files' : files})

@login_required
def submission(request):
	if request.method == 'POST':
		input_report_form = report_input_form(request.POST)
		#input_file_form = FileForm(request.POST, request.FILES)
		if input_report_form.is_valid(): # change this
			# need to do the linking here
			# need to figure out how to do the multiple files
			# figure out how to do required/nonrequired fields with model forms
			# though we could append two forms together, though that is not great

			# how would having non-required fields work?
			current_user = request.user
			profile = UserProfile.objects.filter(user=current_user)
			report_input = Report()
			report_input.author = profile[0]
			report_input.short_description = request.POST['short_description']
			report_input.location = request.POST.get('location','')
			report_input.detailed_description = request.POST['detailed_description']
			#report_input.date_of_incident = request.POST.get('date_of_incident', '2015-03-28')  
			report_input.private = request.POST.get('private', False) #apply a value if it does not exist
			report_input.save()

			for upfile in request.FILES.getlist("file"):
				newfile = File(title = upfile.name, file=upfile, report=report_input)
				newfile.save()

			return HttpResponseRedirect(reverse('report_form.views.submitted'))
	else:
		input_report_form = report_input_form()
		#input_file_form = FileForm()

	return render(request, 'report_form/report_form_template.html', {'input_report_form' : input_report_form})