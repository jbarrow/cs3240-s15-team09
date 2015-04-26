from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.utils.encoding import smart_str

from django.contrib.auth.models import User
from secure_witness.models import UserProfile
from report_form.models import Report, File

from report_form.filter_helper import filter_by_permissions

import json, os
from django.core import serializers
from simplecrypt import encrypt, decrypt
from report_form.views import decrypt_file

def authenticate_with_token(username, token):
    user = User.objects.get(username=username)
    if user != None and user.profile.session_token == token:
        return user
    return None

@csrf_exempt
def auth(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)

    data = {}

    if user is not None:
        if user.is_active:
            profile = user.profile
            profile.session_token = profile.generate_token()
            profile.save()

            data = { "session": profile.session_token }
    else:
        data = { "error": "User does not exist" }

    data = json.dumps(data)

    return HttpResponse(data)

@csrf_exempt
def get_reports(request):
    username = request.POST.get("username")
    token = request.POST.get("token")
    user = authenticate_with_token(username, token)

    if user is None:
        data = { "error": "User does not exist" }
        return HttpResponse(data)

    reports = filter_by_permissions(Report.objects.all(), user)

    data = serializers.serialize("json", reports)
    return HttpResponse(data)

@csrf_exempt
def get_report(request, report_id):
    username = request.POST.get("username")
    token = request.POST.get("token")
    user = authenticate_with_token(username, token)

    if user is None:
        data = { "error": "User does not exist" }
        return HttpResponse(data)

    report = Report.objects.get(pk=report_id)
    if report == None or report.private == True and report.author != user.id:
        data = { "error": "User does not have privilege" }
        return HttpResponse(data)

    data = serializers.serialize("json", [report])
    return HttpResponse(data)

@csrf_exempt
def get_file_list(request, report_id):
    username = request.POST.get("username")
    token = request.POST.get("token")
    user = authenticate_with_token(username, token)

    if user is None:
        data = { "error": "User does not exist" }
        return HttpResponse(data)

    report = Report.objects.get(pk=report_id)
    files = File.objects.filter(report=report)

    data = serializers.serialize("json", files)
    return HttpResponse(data)

@csrf_exempt
def get_file(request, file_id):
    downloadable = get_object_or_404(File, pk=file_id)
    stringkey = downloadable.report.AES_key
    key=stringkey.encode(encoding="iso-8859-1", errors="strict")
    path = downloadable.file.path
    wrapper = FileWrapper(downloadable.file)
    #if private decrypt file
    if downloadable.report.private:
        path = decrypt_file(path, key)
        wrapper=FileWrapper(open(path))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(path))

    return response
