from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from secure_witness.forms import UserForm, UserProfileForm
from secure_witness.models import UserProfile, is_swadmin
from report_form.models import Folder

@login_required
def profile(request):
	form = UserProfileForm()
	if request.method == 'POST':
		form = user_profile_form(request.POST, instance=request.user.profile)
		if form.is_valid():
			print("good")
			form.save()
			return HttpResponseRedirect('/accounts/profile')
		else:
			print("else")
			user = request.user
			profile = user.profile
			form = user_profile_form(instance=profile)

	print(request.method)


	profile = request.user.profile
	user = request.user
    
	return render_to_response('profile.html', {'admin': request.user.is_swadmin, 'name': profile.name, 'user': user, 'form':form})

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

            f = Folder(name = "unsorted", userprofile = profile)
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
