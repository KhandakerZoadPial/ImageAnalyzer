from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
import json
from .models import UserProfile, Plan

# Create your views here.


def login_(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse(json.dumps({'status': "1"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "2"}), content_type="application/json")
    return render(request, 'auth_app/login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        gender = request.POST.get('gender')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password1!=password2:
            return HttpResponse(json.dumps({'status': "1"}), content_type="application/json")
        
        if User.objects.filter(username=username).count() > 0:
            return HttpResponse(json.dumps({'status': "2"}), content_type="application/json")

        user_object = User()
        user_object.username = username
        user_object.first_name = f_name
        user_object.last_name = l_name
        user_object.set_password(password1)
        user_object.save()
        plan_object = Plan()
        plan_object.type_of_plan = 0
        plan_object.save()

        user_profile_object = UserProfile()
        user_profile_object.owner = user_object
        user_profile_object.gender = gender
        user_profile_object.plan = plan_object
        user_profile_object.save()
        # sendmail(user)
        return HttpResponse(json.dumps({'status': "3"}), content_type="application/json")
    else:
        return render(request, 'auth_app/signup.html') 


def logout(request):
    pass