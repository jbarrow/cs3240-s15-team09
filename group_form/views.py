from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from secure_witness.models import UserProfile
from django.contrib.auth.models import User
from group_form.models import Group
from group_form.forms import add_user_group_form
from django.core.exceptions import ObjectDoesNotExist


def add_user_with_form(request):
    context = RequestContext(request)
    current_user = request.user
    current_userprofile = request.user.profile
    form = add_user_group_form(user=current_user)
    # A HTTP POST?
    if request.method == 'POST':
        form = add_user_group_form(request.POST)
        print(form)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form_username = form.cleaned_data['user']
            form_group = form.cleaned_data['group']
            print("adding user")
            g1 = Group.objects.get(name = form_group)
            u1 = User.objects.get(username = form_username)
            g1.users.add(u1)
            return HttpResponseRedirect(reverse('groups:add_user'))
        else:
            print("not valid")
            return HttpResponseRedirect(reverse('groups:add_user'))
            #form data was incorrect


    return render(request, 'group_form/add_user_template.html', {'add_user_group_form' : form})

def add_user(request):
    current_user = request.user.profile
    groups = Group.objects.filter(users=current_user)
    status = ''
    can_add = False

    if request.method == 'POST':
        group_request = request.POST['group']
        if group_request == '':
            status = "Please make a group selection"
            g = None
        else:
            g = Group.objects.get(pk=group_request)
            can_add = True

        members = request.POST['new_members']
        members = members.split(",")
        for x in members:
            x = x.strip()
            if x != '':
                try:
                    user = User.objects.get(username=x)
                    p = UserProfile.objects.get(user=user)
                    if can_add:
                        g.users.add(p)
                        status = user.username + " successfully added"
                    else:
                        status = "group chosen could not be located"
                except ObjectDoesNotExist:
                    status = "User could not be found"

    return render(request, 'group_form/add_user_template.html', {'groups' : groups, 'status': status})