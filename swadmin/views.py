from django.shortcuts import render
from secure_witness.models import is_swadmin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect

@login_required
@user_passes_test(is_swadmin)
def view_users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

@login_required
@user_passes_test(is_swadmin)
def make_admin(request, user_id):
    current = User.objects.filter(id=user_id)[0].profile
    current.admin = True
    current.save()
    return HttpResponseRedirect('/swadmin/users')

@login_required
@user_passes_test(is_swadmin)
def suspend(request, user_id):
    current = User.objects.filter(id=user_id)[0]
    current.is_active = False
    current.save()
    return HttpResponseRedirect('/swadmin/users')
