from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from dashboard.forms import user_profile_form
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    form = user_profile_form()
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
    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('dashboard/profile.html', args)