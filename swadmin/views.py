from django.shortcuts import render
from secure_witness.models import is_swadmin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required

@login_required
@user_passes_test(is_swadmin)
def view_users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

@login_required
@user_passes_test(is_swadmin)
def make_admin(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

@login_required
@user_passes_test(is_swadmin)
def suspend(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})
