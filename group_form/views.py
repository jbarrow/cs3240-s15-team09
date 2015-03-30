from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from group_form.models import Group
from group_form.forms import add_user_group_form

def user_added(request):
	# want to echo back form fields here for confirmation

    return render(request, 'group_form/add_user_template.html', {'add_user' : add_user})


def add_user(request):
    context = RequestContext(request)
    current_user = request.user
    # A HTTP POST?
    if request.method == 'POST':
        form = add_user_group_form(request.POST)
        current_userprofile = UserProfile.objects.filter(user = current_user)
        form.group = UserProfile.groups
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form_username = form.cleaned_data['user']
            form_group = form.cleaned_data['group']
            if User.objects.filter(username = form_username) and Group.objects.filter(name = form_group):
                user1 = User.objects.filter(username = form_username)
                userprofile1 = UserProfile.objects.filter(user = user1)
                g1 = Group.objects.filter(name = form_group)
                userprofile1.groups.add(g1);
                return user_added(request)
            else:

            #form data was incorrect


                return user_added(request)

    else:
        # If the request was not a POST, display the form to enter details.
        form = add_user_group_form()

    return render(request, 'group_form/submission_template.html', {'user_added' : user_added})
