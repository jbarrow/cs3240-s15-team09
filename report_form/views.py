from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from report_form.models import Report, File, ReportForm
from report_form.forms import report_input_form
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def incomplete_landing(request):
	return HttpResponse("Report form not yet available.")

@login_required
def my_reports(request):
	current_user = request.user
	profile = UserProfile.objects.filter(user=current_user)
	my_reports = Report.objects.filter(author=profile[0])
	return render(request, 'report_form/display_list_reports.html', {'my_reports' : my_reports})


@login_required
def detail(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	files = File.objects.filter(report=report)
	return render(request, 'report_form/detail.html', {'report': report, 'files': files})

@login_required
def edit(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	files = File.objects.filter(report=report)
	if request.method == 'POST':
		f = ReportForm(request.POST, instance=report)
		if f.is_valid() and request.POST.get("submission"):
			f.save()
			for upfile in request.FILES.getlist("file"):
				newfile = File(title = upfile.name, file=upfile, report=report)
				newfile.save()

			return HttpResponseRedirect(reverse('report_form.views.detail', args=(report.id,)))
		
		#elif request.POST.get("delete"):
			#return HttpResponse("triggered a delete. Doesn't do anything.")
		else:
			for inputfile in files:
				# delete here
				#print(request.POST.get(inputfile.title))
				if request.POST.get(inputfile.title):
					inputfile.delete()
					return HttpResponseRedirect(reverse('report_form.views.edit', args=(report.id,)))
			
			return HttpResponse("Report form not yet available.")
	else:
		print(request.method)
		f = ReportForm(instance=report)
	return render(request, 'report_form/edit.html', {'input_report_form' : f, 'report': report, 'files': files})


def submitted(request):
	# want to echo back form fields here for confirmation
	submission = Report.objects.latest('id') # this is probably not going to work later
	last_id = submission.id
	files = File.objects.filter(report=submission)
	return render(request, 'report_form/submission_template.html', {'submission' : submission, 'files' : files})

@login_required
def submission(request):
	if request.method == 'POST':
		input_report_form = ReportForm(request.POST)
		#input_file_form = FileForm(request.POST, request.FILES)
		if input_report_form.is_valid(): # change this
			# need to do the linking here
			# need to figure out how to do the multiple files
			# figure out how to do required/nonrequired fields with model forms
			# though we could append two forms together, though that is not great

			# how would having non-required fields work?

			# some of these fields are not really necessary anymore // need to look into it
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
		input_report_form = ReportForm()
		print("has failed in creation")

	return render(request, 'report_form/report_form_template.html', {'input_report_form' : input_report_form})