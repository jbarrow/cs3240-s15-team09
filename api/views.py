from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json

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
