from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
import json
from .models import UserProfile, Plan, Verify

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
        user_profile_object.plan_info = plan_object
        user_profile_object.save()
        verify_send_mail(request, user_profile_object)
        # sendmail(user)
        return HttpResponse(json.dumps({'status': "3"}), content_type="application/json")
    else:
        return render(request, 'auth_app/signup.html') 


def logout(request):
    pass



def verify_account(request, code):
    verify_obj = Verify.objects.filter(code=code)
    if verify_obj.count() > 0:
        verify_obj = verify_obj[0]
        user = verify_obj.whom
        verify_obj.delete()
        messages.success(request, 'Successfully Verified The Account!')
        return redirect('login_')
    else:
        return render(request, 'error.html')






# -----Helpers-----
def send_mail(to, message):
    pass


def code_generator():
    import string
    import random
    return ''.join(random.choices(string.ascii_uppercase +string.digits, k=20))


def verify_send_mail(request, user_profile):
    user_object = user_profile.owner
    if Verify.objects.filter(whom=user_object).count() > 0:
        verify_set = Verify.objects.filter(whom=user_object)
        for item in verify_set:
            item.delete()
        
    code = code_generator()
    while True:
        if Verify.objects.filter(code=code).count() == 0:
            break
        else:
            code = code_generator()
    
    verify_obj = Verify()
    verify_obj.whom = user_object
    verify_obj.code = code
    verify_obj.save()
    urlObject = request.get_host()
    urlObject = urlObject + f'/auth/verify/{code}'
    message_text = 'Please Verify Your Account - '
    message_text = message_text + 'http://'+urlObject
    print(message_text)

    # send_mail(user_object.username, 'Message')

