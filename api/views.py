from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User
from secure_witness.models import UserProfile
from report_form.models import Report

import json
from django.core import serializers

def authenticate_with_token(username, token):
    user = User.objects.get(username=username)
    print(token)
    print(user.profile.session_token)
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

    reports = Report.objects.filter(author=user.profile)

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

    report = Report.objects.filter(author=user.profile, id=report_id)

    data = serializers.serialize("json", report)
    return HttpResponse(data)
