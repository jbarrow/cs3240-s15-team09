from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from report_form.models import Report, File, ReportForm, Folder, TagForm, Tag
from report_form.forms import report_input_form, search_query
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from datetime import date
from django.utils import timezone
from django.core.servers.basehttp import FileWrapper
import os
from report_form.search_helper import simple_return

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
	tags = Tag.objects.filter(associated_report=report)
	return render(request, 'report_form/detail.html', {'report': report, 'files': files, 'tags': tags})

@login_required
def edit(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	files = File.objects.filter(report=report)
	tags = Tag.objects.filter(associated_report=report)
	if request.method == 'POST':
		f = ReportForm(request.POST, instance=report)
		if f.is_valid():
			f.save()
			for upfile in request.FILES.getlist("file"):
				newfile = File(title = upfile.name, file=upfile, report=report)
				newfile.save()
		t = TagForm()
		if t.is_valid:
			if request.POST['keyword'] != '':
				new_tag = Tag(associated_report=report)
				new_tag.keyword = request.POST['keyword']
				new_tag.save()
			if request.POST.get("submission"):	
				return HttpResponseRedirect(reverse('report_form.views.detail', args=(report.id,)))
			else:
				return HttpResponseRedirect(reverse('report_form.views.edit', args=(report.id,)))
		elif request.POST.get("delete"):
			for inputfile in files:
				# delete here
				if request.POST.get(str(inputfile.id)):
					inputfile.delete()
					return HttpResponseRedirect(reverse('report_form.views.edit', args=(report.id,)))
			
			return HttpResponse("Report form not yet available.")
		else:
			return HttpResponse("abnormal.")	

	else:
		print(request.method)
		f = ReportForm(instance=report)
		t = TagForm()
	return render(request, 'report_form/edit.html', {'input_report_form' : f, 'report': report, 'files': files, 'input_tag_form': t, 'tags':tags})


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
		input_tag_form = TagForm(request.POST)
		if input_report_form.is_valid():
			current_user = request.user
			profile = UserProfile.objects.filter(user=current_user)
			unsorted_folder = Folder.objects.get(userprofile=profile, name='unsorted')
			report_input = Report()
			report_input.author = profile[0]
			report_input.short_description = request.POST['short_description']
			report_input.location = request.POST['location']
			report_input.detailed_description = request.POST['detailed_description']
			year = request.POST['date_of_incident_year']
			month = request.POST['date_of_incident_month']
			day = request.POST['date_of_incident_day']
			if year != '0' and month != '0' and day != '0':
				report_input.date_of_incident = date(day= int(day), month=int(month), year=int(year))
			else:
				report_input.date_of_incident = None
			folder_id = request.POST['folder']
			if folder_id == '':
				folder_id = unsorted_folder.id
			report_input.private = request.POST.get('private', False) #apply a value if it does not exist
			report_input.folder = Folder.objects.get(pk=folder_id)
			report_input.save()

			for upfile in request.FILES.getlist("file"):
				newfile = File(title = upfile.name, file=upfile, report=report_input)
				newfile.save()

			if input_tag_form.is_valid():
				newTag = Tag(associated_report=report_input)
				newTag.keyword = request.POST['keyword']
			else:
				print("invalid keyword")

			if(request.POST.get("submission")):
				return HttpResponseRedirect(reverse('report_form.views.detail', args=(report_input.id,)))
			elif(request.POST.get("add_kword")):
				return HttpResponseRedirect(reverse('report_form.views.edit', args=(report_input.id,)))
		else:
			return HttpResponse("form invalid.")
	else:
		input_report_form = ReportForm()
		input_tag_form = TagForm()
		print("has failed in creation")

	return render(request, 'report_form/report_form_template.html', {'input_report_form' : input_report_form, 'input_tag_form' : input_tag_form})

@login_required
def download(request, file_id):
	# TODO: Verify that the user is only downloading allowed files (i.e. not
	# server source files, etc.)
	downloadable = get_object_or_404(File, pk=file_id)
	path = downloadable.file.path
	wrapper = FileWrapper(downloadable.file)
	response = HttpResponse(wrapper, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(path))
	#print(response['Content-Disposition'])
	return response

@login_required
def simple_search(request):
	if request.method == 'POST':
		s = search_query(request.POST)
		if s.is_valid():
			print(simple_return(request.POST['category'], request.POST['search_input']))
	else:
		s = search_query()
		print("didn't post")
	return render(request, 'report_form/search_form.html', {'search_form' : s})
