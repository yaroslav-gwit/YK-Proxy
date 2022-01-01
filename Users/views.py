from django.shortcuts import render, redirect
from django.db.models import F
from pathlib import Path
import os
from HAProxyManager import settings
from Users import models as user_models
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User as system_users

# Create your views here.
def users(request):
    page_name = "Users"
    users = user_models.User.objects.order_by(F('full_name').asc())
    # users = user_models.User.objects.all
    context = {
        'page_name': page_name,
        'users': users,
    }
    
    return render(request, "Users/main.html", context)

def delete_user(request, username, ):
    select_system_user = system_users.objects.get(username=username)
    select_username = user_models.User.objects.get(username=username)
    select_system_user.delete()
    select_username.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def disable_user(request, username, disabled_status):
    select_system_user = system_users.objects.get(username=username)
    select_username = user_models.User.objects.get(username=username)
    if disabled_status == "No":
        disable = "Yes"
        system_user_active = False
    else:
        disable = "No"
        system_user_active = True
    select_username.disabled = disable
    select_system_user.is_active = system_user_active
    select_username.save(update_fields=['disabled'])
    select_system_user.save(update_fields=['is_active'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create_new_user(request):
    users_last_id = user_models.User.objects.order_by(F('user_id').desc())[0]
    firstName = ""
    lastName = ""
    full_name = ""
    email = ""
    username = ""
    password = ""
    user_id = ""
    user_role = ""
    success_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('FirstName')
        last_name = request.POST.get('LastName')
        full_name = first_name + " " + last_name
        email = request.POST.get('Email')
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user_id = request.POST.get('UserId')
        user_role = request.POST.get('UserRole')
        
        save_user = user_models.User.objects.create(full_name=full_name, username=username, user_id=user_id, email=email, role=user_role, )
        save_system_user = system_users.objects.create_user(username, email, password)
        save_system_user.last_name = last_name
        save_system_user.first_name = first_name
        save_system_user.save()

        success_message = "User " + username + " was created!"

    page_name = "Create new user"
    context = {
        'page_name': page_name,
        'success_message': success_message,
        'users_last_id':users_last_id
    }

    return render(request, "Users/users_create_new_user.html", context)