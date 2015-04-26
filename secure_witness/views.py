from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from secure_witness.forms import UserForm, UserProfileForm, user_profile_form
from secure_witness.models import UserProfile, is_swadmin
from report_form.models import Folder
from group_form.models import Group
from  django.contrib.auth.hashers import check_password
import re
@login_required
def profile(request):
    form = user_profile_form()
    form2 = UserForm()
    status = "Edit profile below:"
    user = request.user
    profile = request.user.profile
    groups = Group.objects.filter(users=profile)
    a = re.compile(r'^[\w.@+-]+$')

    if request.method == 'POST':
        if check_password(request.POST['conf_password'], user.password):
            form = user_profile_form(request.POST, instance=request.user.profile)
            form2 = UserForm(request.POST, instance=request.user)
            if request.POST['name'] != '':
                profile.name = request.POST['name'].strip()
            profile.save()
            if request.POST['password'] != '':
                user.password = request.POST['password']
                user.set_password(user.password)
            if request.POST['email'] != '':
                user.email = request.POST['email'].strip()
            if request.POST['username'] != '':
                if len(request.POST['username']) > 30 or not a.match(request.POST['username']):
                    status = "Invalid username."
                    return render(request, 'profile.html',
                  {'form':form, 'groups':groups, 'form2':form2, 'status':status})
                user.username = request.POST['username'].strip()
            user.save()
            status = "Profile update successful."
            #return HttpResponseRedirect('/accounts/profile')
        else:
            status = "Password invalid."



    return render(request, 'profile.html',
                  {'form':form, 'groups':groups, 'form2':form2, 'status':status})


def base(request):
    profile = request.user.profile
    user = request.user
    return render_to_response('base.html', {'admin': request.user.is_swadmin, 'name': profile.name, 'user': user})


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

            f = Folder(name="unsorted", userprofile=profile)
            f.save()
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('registration/register.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                              context)


@login_required
@user_passes_test(is_swadmin)
def admin_test(request):
    print("ADMIN!")
    return render_to_response('profile.html', {'admin': request.user.is_swadmin, 'name': request.user.profile.name})
