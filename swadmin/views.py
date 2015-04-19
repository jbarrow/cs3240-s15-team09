from django.shortcuts import render
from secure_witness.models import is_swadmin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from group_form.models import Group

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
    users = User.objects.all()
    if request.method == "POST":
        name = request.POST["group_name"]
        users = request.POST.getlist("users")

        g = Group(name=name)
        g.save()

        for user in users:
            user = user.strip()
            u = User.objects.get(pk=user)
            g.users.add(u)

        return HttpResponseRedirect('/swadmin/groups')
    else:
        return render(request, 'create_group.html', {'user': current, 'users': users})

@login_required
@user_passes_test(is_swadmin)
def delete_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    group.delete()
    return HttpResponseRedirect('/swadmin/groups')
