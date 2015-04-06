from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from secure_witness.forms import UserForm, UserProfileForm
from secure_witness.models import UserProfile

def profile(request):
    profile = UserProfile.objects.filter(user=request.user)
    print(request.user)
    print(profile[0].admin)
    return render_to_response('profile.html', {'admin': profile[0].admin, 'name': profile[0].name})

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        print("Before")

        if user_form.is_valid() and profile_form.is_valid():
            print("Valid")
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            print("Save")

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('registration/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)
