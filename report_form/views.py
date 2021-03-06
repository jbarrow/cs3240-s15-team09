from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render_to_response

from django.core.context_processors import csrf

from report_form.models import Report, File, ReportForm, Folder, TagForm, Tag, Permission
from report_form.forms import report_input_form, multi_cat_search_query, single_search_query, \
    multi_field_multi_cat_search, new_folder_form
from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from datetime import date
from django.utils import timezone
from django.core.servers.basehttp import FileWrapper
from group_form.models import Group
from report_form.filter_helper import filter_by_permissions, get_shared_reports, get_5_latest

import os
from report_form.search_helper import simple_return, multi_cat_return, string_parse, advanced_query, multi_cat_return_OR
from Crypto.Cipher import AES
from Crypto import Random
import os
from simplecrypt import encrypt, decrypt
from secure_witness.settings import MEDIA_ROOT
from report_form.validation_helper import permission_validation
from report_form.cryptohelper import get_file_checksum


def incomplete_landing(request):
    return HttpResponse("Report form not yet available.")


@login_required
def my_reports(request, user_id):
    current_user = request.user
    profile = UserProfile.objects.get(user=current_user)
    my_reports = Report.objects.filter(author=profile)
    if request.method == 'POST':
        for indiv in my_reports:
            output = str(indiv.id)
            copy = output + "_copy"
            if request.POST.get(output):
                report_files = File.objects.filter(report=indiv)
                for indiv_file in report_files:
                    indiv_file.delete()
                report_tags = Tag.objects.filter(associated_report=indiv)
                for indiv_tag in report_tags:
                    indiv_tag.delete()
                indiv.delete()
                # want to delete only one at a time
                return HttpResponseRedirect(reverse('report_form:my_reports', args=(profile.user.id,)))
            elif request.POST.get(copy):
                copy_report(indiv.id, profile)
                return HttpResponseRedirect(reverse('report_form:my_reports', args=(profile.user.id,)))
    return render(request, 'report_form/display_list_reports.html', {'my_reports': my_reports, 'profile': profile})


def copy_report(indiv_id, profile):
    print("copy report")
    report = get_object_or_404(Report, pk=indiv_id)
    files = File.objects.filter(report=report)
    tags = Tag.objects.filter(associated_report=report)
    perm = get_object_or_404(Permission, report=report)
    # print(perm)
    r = Report()
    r.author = report.author
    r.short_description = report.short_description
    r.location = report.location
    r.detailed_description = report.detailed_description
    r.private = report.private
    unsorted_folder = Folder.objects.get(userprofile=profile, name='unsorted')
    r.folder = unsorted_folder
    r.save()
    for element in tags:
        t = Tag(associated_report=r)
        t.keyword = element.keyword
        t.save()
    for x in files:
        f = File(report=r)
        f.file = x.file
        f.title = x.title
        f.hash_code = x.hash_code
        f.save()
    p = Permission(report=r)
    print(p)
    p.save()
    for g in perm.groups.all():
        p.groups.add(g)
    for v in perm.profiles.all():
        p.profiles.add(v)
    p.save()


@login_required
def detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    files = File.objects.filter(report=report)
    tags = Tag.objects.filter(associated_report=report)
    p = Permission.objects.filter(report=report)
    return render(request, 'report_form/detail.html', {'report': report, 'files': files, 'tags': tags, 'p': p[0], })


@login_required
def edit(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    is_private = report.private
    files = File.objects.filter(report=report)
    tags = Tag.objects.filter(associated_report=report)
    perm = get_object_or_404(Permission, report=report)
    current_user = request.user
    profile = UserProfile.objects.filter(user=current_user)
    groups = Group.objects.filter(users=profile[0])
    if request.method == 'POST':
        request.POST['private'] = is_private
        f = ReportForm(request.POST, instance=report)
        if f.is_valid():
            f.save()
            if report.private:
                #print("encrypt the file")
                for each in request.FILES.getlist("file"):
                    stringkey = report.AES_key
                    key = stringkey.encode(encoding="iso-8859-1", errors="strict")
                    encrypt_file(each, key)
                    newfile = File(title=each.name + ".enc", file=each.name + ".enc", report=report)
                    newfile.save()
                    #newfile = File(title = each.name+".enc", file=each.name+".enc", report=report_input, AES_key=key)
            else:
                for upfile in request.FILES.getlist("file"):
                    newfile = File(title=upfile.name, file=upfile, report=report)
                    newfile.save()
                    path = newfile.file.path
                    hash_code = get_file_checksum(path)
                    newfile.hash_code = hash_code
                    newfile.save()
                    print("from edit " + newfile.hash_code + "****")

            t = TagForm()
            if t.is_valid:
                if request.POST['keyword'] != '':
                    new_tag = Tag(associated_report=report)
                    new_tag.keyword = request.POST['keyword']
                    new_tag.save()
                    # need to alter so that you can add AND DELETE
            viewers = request.POST["viewers"]
            viewers = viewers.split(",")
            g = request.POST.getlist("group_names")
            print(g)
            print(viewers)
            for y in viewers:
                y = y.strip()
                if y != '':
                    status = permission_validation(y, perm.id)
                    print("From edit, status")
                    print(status)
            # issues with addition and deletion is unimplemented
            for x in g:
                x = x.strip()
                gr = Group.objects.get(pk=x)
                perm.groups.add(gr)
            perm.save()

        if request.POST.get("submission"):
            return HttpResponseRedirect(reverse('report_form:detail', args=(report.id,)))
        elif request.POST.get("delete"):
            for inputfile in files:
                # delete here
                if request.POST.get(str(inputfile.id)):
                    inputfile.delete()
                    return HttpResponseRedirect(reverse('report_form:edit', args=(report.id,)))

            return HttpResponse("Report form not yet available.")
        elif request.POST.get("add_kword"):
            return HttpResponseRedirect(reverse('report_form:edit', args=(report.id,)))
        print(request.POST)
        for k in perm.groups.all():
            key = str(k.id)
            key += "_group"
            print(key)
            if request.POST.get(key):
                perm.groups.remove(k)
                perm.save()
                return HttpResponseRedirect(reverse('report_form:edit', args=(report.id,)))
        for m in perm.profiles.all():
            key = str(m.user.id)
            key += "_profile"
            print(key)
            if request.POST.get(key):
                perm.profiles.remove(m)
                perm.save()
                return HttpResponseRedirect(reverse('report_form:edit', args=(report.id,)))
        for t in Tag.objects.all():
            key = str(t.id)
            key += "_kword"
            if request.POST.get(key):
                t.delete()
                return HttpResponseRedirect(reverse('report_form:edit', args=(report.id,)))
        for fi in File.objects.all():
            key = str(fi.id)
            key += "_delete"
            if request.POST.get(key):
                fi.delete()
                return HttpResponseRedirect(reverse('report_form:edit', args=(report.id,)))

        else:
            print(request.POST)
            return HttpResponse("unexpected input widget")
    else:
        print(request.method)
        f = ReportForm(instance=report)
        t = TagForm()

    return render(request, 'report_form/edit.html',
                  {'input_report_form': f, 'report': report, 'files': files, 'input_tag_form': t, 'tags': tags,
                   'groups': groups, 'p': perm})


def submitted(request):
    # want to echo back form fields here for confirmation
    submission = Report.objects.latest('id')  # this is probably not going to work later
    last_id = submission.id
    files = File.objects.filter(report=submission)
    return render(request, 'report_form/submission_template.html', {'submission': submission, 'files': files})


@login_required
def submission(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user=current_user)
    groups = Group.objects.filter(users=profile[0])
    if request.method == 'POST':
        input_report_form = ReportForm(request.POST)
        input_tag_form = TagForm(request.POST)
        if input_report_form.is_valid():
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
                report_input.date_of_incident = date(day=int(day), month=int(month), year=int(year))
            else:
                report_input.date_of_incident = None
            folder_id = request.POST['folder']
            if folder_id == '':
                folder_id = unsorted_folder.id
            report_input.private = request.POST.get('private', False)  # apply a value if it does not exist
            report_input.folder = Folder.objects.get(pk=folder_id)
            # report_input.save()

            key = random_key = os.urandom(16)
            print(type(key))
            print(key)
            stringkey = key.decode(encoding="iso-8859-1", errors="strict")
            print(type(stringkey))
            #print(stringkey)
            report_input.AES_key = stringkey
            report_input.save()

            encrypt_error = False

            if report_input.private:
                #print("encrypt the file")
                try:
                    for each in request.FILES.getlist("file"):
                        stringkey = report_input.AES_key
                        key = stringkey.encode(encoding="iso-8859-1", errors="strict")
                        encrypt_file(each, key)
                        newfile = File(title=each.name + ".enc", file=each.name + ".enc", report=report_input)
                        newfile.save()
                        path = newfile.file.path
                        hash_code = get_file_checksum(path)
                        newfile.hash_code = hash_code
                        newfile.save()
                        print("from encrypted submit: " + newfile.hash_code + "*****")
                #newfile = File(title = each.name+".enc", file=each.name+".enc", report=report_input, AES_key=key)
                except UnicodeDecodeError:
                    encrypt_error = True
            if not report_input.private or encrypt_error:
                for upfile in request.FILES.getlist("file"):
                    newfile = File(title=upfile.name, file=upfile, report=report_input)
                    newfile.save()
                    path = newfile.file.path
                    #print("path:")
                    #print(path)
                    #print(os.path.basename(path))
                    hash_code = get_file_checksum(path)
                    newfile.hash_code = hash_code
                    newfile.save()
                    print("from submit: " + newfile.hash_code + "*****")
                    #print("******************************")
                    #print(get_file_checksum(upfile))
                #newfile = File(title = upfile.name, file=upfile, report=report_input, AES_key=key)



            if input_tag_form.is_valid():
                newTag = Tag(associated_report=report_input)
                newTag.keyword = request.POST['keyword']
                if newTag.keyword != '':
                    newTag.save()
            else:
                print("invalid keyword")

            # a permissions object is created for every report regardless of anything really
            permission_object = Permission(report=report_input)
            permission_object.save()
            viewers = request.POST["viewers"]
            viewers = viewers.split(",")
            g = request.POST.getlist("group_names")
            print(viewers)
            print(g)

            for y in viewers:
                y = y.strip()
                if y != '':
                    print("status from submission")
                    status = permission_validation(y, permission_object.id)
                    print(status)
            for x in g:
                x = x.strip()
                gr = Group.objects.get(pk=x)
                permission_object.groups.add(gr)
            permission_object.save()

            if (request.POST.get("submission")):
                return HttpResponseRedirect(reverse('report_form:detail', args=(report_input.id,)))
            elif (request.POST.get("add_kword")):
                return HttpResponseRedirect(reverse('report_form:edit', args=(report_input.id,)))
    else:
        input_report_form = ReportForm()
        input_tag_form = TagForm()

    return render(request, 'report_form/report_form_template.html',
                  {'input_report_form': input_report_form, 'input_tag_form': input_tag_form, 'groups': groups})


def encrypt_file(file_name, key):
    # with open(file_name, 'rb') as fo:
    plaintext = file_name.read()
    #print(plaintext)
    print("Text to encrypt: %s" % plaintext)
    print("about to encrypt")
    print(key)
    enc = encrypt(key, plaintext)
    with open("media/" + file_name.name + ".enc", 'wb') as fo:
        fo.write(enc)


def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(key, ciphertext)  # .decode('iso-8859-1')
    print("decrypted text: %s" % dec)
    with open(file_name[:-4], 'wb') as fo:
        # fo.write(bytes(dec, 'utf8'))
        fo.write(dec)
    # print()
    return file_name[:-4]


@login_required
def download(request, file_id):
    downloadable = get_object_or_404(File, pk=file_id)
    stringkey = downloadable.report.AES_key
    error_decrypt = False
    key = stringkey.encode(encoding="iso-8859-1", errors="strict")
    #print(stringkey)
    print("key is: ")
    print(key)
    path = downloadable.file.path
    wrapper = FileWrapper(downloadable.file)

    if downloadable.report.private:
        print("about to decrypt")
        print(key)
        print(path)
        path = decrypt_file(path, key)
        wrapper = FileWrapper(open(path, 'rb'))
        print(path)

    check_sum_hash = downloadable.hash_code
    check_against = get_file_checksum(path)
    print("in downloads: check hash")
    print(check_against == check_sum_hash)

    try:
        response = HttpResponse(wrapper, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment;filename=%s' % smart_str(os.path.basename(path))
    except UnicodeDecodeError:
        error_decrypt = True

    if error_decrypt:
        response = HttpResponse("error in decryption - file could not be processed")
    elif check_sum_hash != check_against and not downloadable.report.private:
        response = HttpResponse("Stored Hash: \"" + check_sum_hash + "\" does not match generated Hash: \"" + check_against +"\"")
    
    return response


# for each in Report.objects.all():
#		report_files=File.objects.filter(report=each)
#		for a_file in report_files:
#			if a_file.file_id==file_id:
# #				key=each.AESkey
# #				break
# #	
# #	# TODO: Verify that the user is only downloading allowed files (i.e. not
# 	# server source files, etc.)
# 	downloadable = get_object_or_404(File, pk=file_id)
#     #print(downloadable.report)
# #	for each in Report.objects.all():
# #		report_files=File.objects.filter(report=each)
# #		for a_file in report_files:
# #			if a_file.file_id==file_id:
# #				key=each.AESkeyss
# #				breaks

# 	key= downloadable.report.AES_key
# 	print(key)
#     path = downloadable.file.path
# 	wrapper = FileWrapper(downloadable.file)
# if downloadable.report.private:

#         decrypt_file(path,key)
# response = HttpResponse(wrapper, content_type='application/force-download')
# response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(path))
#print(response['Content-Disposition'])
# return response


@login_required
#  not really used anymore
def simple_search(request):
    results = []
    public_only = True
    if request.method == 'POST':
        s = multi_cat_search_query(request.POST)
        if s.is_valid():
            query = request.POST['search_input'].strip()
            results = multi_cat_return(request.POST.getlist("category"), query)
            return render(request, 'report_form/search_form.html',
                          {'search_form': s, 'results': results, 'public_only': public_only,
                           'query_string': query, 'empty': False, 'link': 'simple_search'})
    else:
        s = multi_cat_search_query()

    return render(request, 'report_form/search_form.html',
                  {'search_form': s, 'results': results, 'public_only': public_only,
                   'query_string': "", 'empty': True, 'link': 'simple_search'})


@login_required
def advanced_search(request):
    current_user = request.user
    results = []
    public_only = False
    if request.method == 'POST':
        s = multi_field_multi_cat_search(request.POST)
        if s.is_valid():
            search_queries = []
            search_queries.append(request.POST['s_author'].strip())
            search_queries.append(request.POST['s_short_desc'].strip())
            search_queries.append(request.POST['s_location'].strip())
            search_queries.append(request.POST['s_detailed_desc'].strip())
            search_queries.append(request.POST['s_keyword'].strip())
            search_queries.append(request.POST['s_date_year'].strip())
            search_queries.append(request.POST['s_date_month'].strip())
            search_queries.append(request.POST['s_date_day'].strip())
            results = advanced_query(search_queries)
            results = list(results)
            results.append(current_user)
            return render(request, 'report_form/search_form.html',
                          {'search_form': s, 'results': results, 'public_only': public_only,
                           'query_string': "Advanced Search", 'empty': False, 'link': 'report_form:advanced_search'})
    else:
        s = multi_field_multi_cat_search()
    return render(request, 'report_form/search_form.html',
                  {'search_form': s, 'results': results, 'public_only': public_only,
                   'query_string': "", 'empty': True, 'link': 'report_form:advanced_search'})


@login_required
def search_with_OR(request):
    current_user = request.user
    results = []
    public_only = False
    if request.method == 'POST':
        s = multi_cat_search_query(request.POST)
        if s.is_valid():
            query = request.POST['search_input'].strip()
            print(query)
            query_set_or = string_parse(" OR ", query)
            print(query_set_or)
            if len(query_set_or) > 0:
                results = multi_cat_return_OR(request.POST.getlist("category"), query_set_or)
            else:
                results = multi_cat_return(request.POST.getlist("category"), query)
            results = list(results)
            results.append(current_user)
            print(results)
            return render(request, 'report_form/search_form.html',
                          {'search_form': s, 'results': results, 'public_only': public_only,
                           'query_string': query, 'empty': False, 'link': 'report_form:search_with_OR'})
    else:
        s = multi_cat_search_query()

    return render(request, 'report_form/search_form.html',
                  {'search_form': s, 'results': results, 'public_only': public_only,
                   'query_string': "", 'empty': True, 'link': 'report_form:search_with_OR'})


@login_required
def new_folder(request):
    current_userprofile = request.user.profile
    unsorted_folder = Folder.objects.get(userprofile=current_userprofile, name="unsorted")
    unsorted_reports = Report.objects.filter(folder=unsorted_folder)
    if request.method == "POST":
        folder_name = request.POST["folder_name"]
        selected_reports = request.POST.getlist('selected_reports')  # list containing all report ids

        f = Folder(userprofile=current_userprofile, name=folder_name)
        f.save()
        print(selected_reports)
        for report_id in selected_reports:
            report = Report.objects.get(author=current_userprofile, pk=report_id)
            report.folder = Folder.objects.get(userprofile=current_userprofile, name=folder_name)

            report.save()

        return HttpResponseRedirect(reverse('report_form:folder_detail', args=(f.id,)))
    else:
        return render(request, 'report_form/create_folder.html', {'user': current_userprofile,
                                                                  'reports': unsorted_reports}, )


@login_required
def delete_folder(request, folder_id):
    current_userprofile = request.user.profile
    folder = Folder.objects.get(userprofile=current_userprofile, pk=folder_id)
    reports_in_folder = Report.objects.filter(folder=folder)

    for report in reports_in_folder:
        report.folder = Folder.objects.get(userprofile=current_userprofile, name="unsorted")
        report.save()
    folder.delete()
    return HttpResponseRedirect(reverse('report_form:my_reports', args=(current_userprofile.user.id,)))


@login_required
def folder_detail(request, folder_id, ):
    folder = get_object_or_404(Folder, pk=folder_id)
    current_user = request.user

    profile = current_user.profile
    reports_in_folder = Report.objects.filter(author=profile, folder=folder)
    all_folders = Folder.objects.filter(userprofile=profile, )

    if request.method == 'POST':
        for indiv in reports_in_folder:
            output = str(indiv.id)
            copy = output + "_copy"
            folder_input = output + "_folder"
            if request.POST.get(output):
                report_files = File.objects.filter(report=indiv)
                for indiv_file in report_files:
                    indiv_file.delete()
                report_tags = Tag.objects.filter(associated_report=indiv)
                for indiv_tag in report_tags:
                    indiv_tag.delete()
                indiv.delete()
                # want to delete only one at a time
                return HttpResponseRedirect(reverse('report_form:folder_detail', args=(folder.id,), ))
            elif request.POST.get(folder_input):
                unsorted_folder = Folder.objects.get(userprofile=profile, name="unsorted")
                indiv.folder = unsorted_folder
                indiv.save()
                return HttpResponseRedirect(reverse('report_form:folder_detail', args=(folder.id,), ))

    return render(request, 'report_form/folder_detail.html',
                  {'reports_in_folder': reports_in_folder, 'profile': profile, 'folder': folder, }, )


@login_required
def edit_folder(request, folder_id):
    current_userprofile = request.user.profile
    unsorted_folder = Folder.objects.get(userprofile=current_userprofile, name="unsorted")
    unsorted_reports = Report.objects.filter(folder=unsorted_folder)
    current_folder = Folder.objects.get(userprofile=current_userprofile, pk=folder_id)
    if request.method == "POST":
        folder_name = request.POST["folder_name"]
        selected_reports = request.POST.getlist('selected_reports')  # list containing all report ids
        if folder_name != "":
            current_folder.name = folder_name
            current_folder.save()
        for report_id in selected_reports:
            report = Report.objects.get(author=current_userprofile, pk=report_id)
            report.folder = current_folder

            report.save()

        return HttpResponseRedirect(reverse('report_form:folder_detail', args=(current_folder.id,)))
    else:
        return render(request, 'report_form/edit_folder.html', {'user': current_userprofile,
                                                                'reports': unsorted_reports, 'folder': current_folder})


@login_required
def view_all_available(request):
    current_user = request.user
    reports = Report.objects.all()
    reports = get_shared_reports(reports, current_user)
    #reports = list(reports)
    #reports.append(current_user)
    #return render(request, 'report_form/view_all.html', {'list_reports': reports, 'user': current_user})
    return render(request, 'report_form/view_shared_latest.html', {'list_reports': reports, 'filter': 'shared'})


@login_required
def latest_5(request):
    current_user = request.user
    reports = Report.objects.all()
    reports = get_5_latest(reports, current_user)
    #reports = list(reports)
    #reports.append(current_user)
    #return render(request, 'report_form/view_all.html', {'list_reports': reports, 'user': current_user})
    return render(request, 'report_form/view_shared_latest.html', {'list_reports': reports, 'filter': 'latest'})


@login_required
def view_all_available_dynamic(request):
    current_user = request.user
    profile = current_user.profile
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
    if request.method == 'POST':
        sort_request = request.POST['sort']
        if sort_request == "Default":
            all_reports = all_reports
        elif sort_request == "location_az":

            all_reports = all_reports.order_by('location', 'short_description')
        elif sort_request == "location_za":
            all_reports = all_reports.order_by('-location', 'short_description')
        elif sort_request == "author_az":
            all_reports = all_reports.order_by('author', 'short_description')
        elif sort_request == "author_za":
            all_reports = all_reports.order_by('-author', 'short_description')
        elif sort_request == "shortdes_az":
            all_reports = all_reports.order_by('short_description', '-time_created')
        elif sort_request == "shortdes_za":
            all_reports = all_reports.order_by('-short_description', '-time_created')
        elif sort_request == "created_new":
            all_reports = all_reports.order_by('-time_created', 'short_description')
        elif sort_request == "created_old":
            all_reports = all_reports.order_by('time_created', 'short_description')
        elif sort_request == "date_of_incident_new":
            all_reports = all_reports.order_by('-date_of_incident', 'short_description')
        elif sort_request == "date_of_incident_old":
            all_reports = all_reports.order_by('date_of_incident', 'short_description')
    return render(request, 'report_form/view_all_dynamic.html', {'list_reports': all_reports, 'filter': 'shared'})

