from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from report_form.models import Report, File, ReportForm, Folder
from report_form.forms import report_input_form
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
import datetime
from django.utils import timezone
from django.core.servers.basehttp import FileWrapper
import os

def incomplete_landing(request):
	return HttpResponse("Report form not yet available.")

@login_required
def my_reports(request, user_id):
	current_user = request.user
	profile = UserProfile.objects.filter(user=current_user)
	my_reports = Report.objects.filter(author=profile[0])
	if request.method == 'POST':
		for indiv in my_reports:
			if request.POST.get(str(indiv.id)):
				report_files = File.objects.filter(report=indiv)
				for indiv_file in report_files:
					indiv_file.delete()
				indiv.delete()
				# want to delete only one at a time
				return HttpResponseRedirect(reverse('report_form.views.my_reports', args=(profile[0].user.id,)))
	return render(request, 'report_form/display_list_reports.html', {'my_reports' : my_reports, 'profile': profile[0]})


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
		else:
			for inputfile in files:
				# delete here
				#print(request.POST.get(inputfile.title))
				if request.POST.get(str(inputfile.id)):
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
			current_user = request.user
			profile = UserProfile.objects.filter(user=current_user)
			unsorted_folder = Folder.objects.get(userprofile=profile, name='unsorted')
			report_input = Report()
			report_input.author = profile[0]
			report_input.short_description = request.POST['short_description']
			report_input.location = request.POST.get('location','')
			report_input.detailed_description = request.POST['detailed_description']
			#if request.POST['date_of_incident'] == '':
			#	report_input.date_of_incident = datetime.date.today()
			#else:
			#	print("need validity check here anyway")
			#	report_input.date_of_incident = request.POST['date_of_incident']
			folder_id = request.POST['folder']
			if folder_id == '':
				folder_id = unsorted_folder.id
			report_input.private = request.POST.get('private', False) #apply a value if it does not exist
			report_input.folder = Folder.objects.get(pk=folder_id)
			report_input.save()

			for upfile in request.FILES.getlist("file"):
				newfile = File(title = upfile.name, file=upfile, report=report_input)
				newfile.save()

			return HttpResponseRedirect(reverse('report_form.views.detail', args=(report_input.id,)))
		else:
			return HttpResponse("form invalid.")
	else:
		input_report_form = ReportForm()
		print("has failed in creation")

	return render(request, 'report_form/report_form_template.html', {'input_report_form' : input_report_form})

@login_required
def download(request, file_id):
	# TODO: Verify that the user is only downloading allowed files (i.e. not
	# server source files, etc.)
	# chosen_files = File.objects.filter(title=smart_str(request.GET.get('n')))
	# downloadable = chosen_files[0]
	downloadable = get_object_or_404(File, pk=file_id)
	path = downloadable.file.path
	wrapper = FileWrapper(downloadable.file)
	response = HttpResponse(wrapper, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(path))
	print(response['Content-Disposition'])
	#response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(request.GET.get('n'))
	#response['X-Sendfile'] = smart_str(request.GET.get('f'))
	return response
