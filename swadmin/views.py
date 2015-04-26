from django.shortcuts import render
from secure_witness.models import is_swadmin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from group_form.models import Group
from report_form.models import Report, Tag, File
from secure_witness.models import UserProfile

@login_required
@user_passes_test(is_swadmin)
def view_users(request):
    users = User.objects.all()
    user = request.user
    return render(request, 'users.html', {'users': users, 'user': request.user})

@login_required
@user_passes_test(is_swadmin)
def make_admin(request, user_id):
    current = User.objects.filter(id=user_id)[0].profile
    current.admin = True
    current.is_active = True
    current.save()
    return HttpResponseRedirect('/swadmin/users')

@login_required
@user_passes_test(is_swadmin)
def suspend(request, user_id):
    current = User.objects.filter(id=user_id)[0]
    current.is_active = False
    current.save()
    return HttpResponseRedirect('/swadmin/users')

@login_required
@user_passes_test(is_swadmin)
def unsuspend(request, user_id):
    current = User.objects.filter(id=user_id)[0]
    current.is_active = True
    current.save()
    return HttpResponseRedirect('/swadmin/users')

@login_required
@user_passes_test(is_swadmin)
def view_groups(request):
    groups = Group.objects.all()
    user = request.user
    return render(request, 'groups.html', {'groups': groups, 'user': request.user})

@login_required
@user_passes_test(is_swadmin)
def create_group(request):
    current = request.user
    users = UserProfile.objects.all()
    if request.method == "POST":
        name = request.POST["group_name"]
        users = request.POST.getlist("users")

        g = Group(name=name)
        g.save()

        for user in users:
            user = user.strip()
            u = UserProfile.objects.get(pk=user)
            g.users.add(u)

        return HttpResponseRedirect('/swadmin/groups')
    else:
        return render(request, 'create_group.html', {'user': current, 'users': users})

@login_required
@user_passes_test(is_swadmin)
def edit_group(request, group_id):
    current = request.user
    g = Group.objects.get(pk=group_id)
    users_in_group = g.users.all()
    other_users = UserProfile.objects.all()
    for cur_user in users_in_group:
        other_users = other_users.exclude(pk = cur_user.pk)

    if request.method == "POST":
        users_to_delete = request.POST.getlist("users_to_delete")
        users_to_add = request.POST.getlist("users_to_add")

        for user in users_to_delete:
            user = user.strip()
            u = UserProfile.objects.get(pk=user)
            g.users.remove(u)

        for user in users_to_add:
            user = user.strip()
            u = UserProfile.objects.get(pk=user)
            g.users.add(u)

        return HttpResponseRedirect('/swadmin/groups')
    else:
        return render(request, 'edit_group.html', {'user': current, 'users_in_group': users_in_group
            , 'other_users': other_users, 'group': g,})

@login_required
@user_passes_test(is_swadmin)
def delete_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    group.delete()
    return HttpResponseRedirect('/swadmin/groups')

@login_required
@user_passes_test(is_swadmin)
def view_all_reports(request):
    all_reports = Report.objects.all()
    # need to redirect to details
    if request.method == 'POST':
        for indiv in all_reports:
            output = str(indiv.id)
            if request.POST.get(output):
                report_files = File.objects.filter(report=indiv)
                for indiv_file in report_files:
                    indiv_file.delete()
                report_tags = Tag.objects.filter(associated_report=indiv)
                for indiv_tag in report_tags:
                    indiv_tag.delete()
                indiv.delete()
                # want to delete only one at a time
                return HttpResponseRedirect('/swadmin/reports')
        
    return render(request, 'list_reports.html', {'my_reports' : all_reports})  
