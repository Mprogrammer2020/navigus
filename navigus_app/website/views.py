from django.shortcuts import render
from django.template.context_processors import request
from django.db import transaction
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

def index(request):
    with transaction.atomic():
        token = None
        try:
            token = request.session['token']
            token1 = Token.objects.get(key=token)
            user = token1.user
            checkGroup1 = user.is_superuser
            checkGroup2 = user.groups.filter(name='teacher').exists()
            checkGroup3 = user.groups.filter(name='student').exists()
            if checkGroup1:
                return render(request, "admin/dashboard.html", {"token":token})
            elif checkGroup2:
                return render(request, "teacher/dashboard.html", {"token":token})
            elif checkGroup3:
                return render(request, "student/dashboard.html", {"token":token})
            else:
                if request.session.get('token', False):
                    del request.session['token']
                return redirect("index")
        except:
            token = None
            return render(request, "login.html",)
        
def dashboard(request):
    with transaction.atomic():
        token = None
        if 'token' in request.POST.keys():
            token = request.POST['token']
            request.session['token'] = token
        if token is None and request.session['token'] is not None:
            token = request.session['token']
        if token is not None:
            token1 = Token.objects.get(key=token)
            user = token1.user
            checkGroup1 = user.is_superuser
            checkGroup2 = user.groups.filter(name='teacher').exists()
            checkGroup3 = user.groups.filter(name='student').exists()
            if checkGroup1:
                return render(request, "admin/dashboard.html", {"token":token})
            elif checkGroup2:
                return render(request, "teacher/dashboard.html", {"token":token})
            elif checkGroup3:
                return render(request, "student/dashboard.html", {"token":token})
            else:
                if request.session.get('token', False):
                    del request.session['token']
                return redirect("index")
        else:
            if request.session.get('token', False):
                del request.session['token']
            return redirect("index")
        
def signuptemplate(request):
    return render(request, "signup.html", {})

def students(request):
    with transaction.atomic():
        token = None
        if 'token' in request.POST.keys():
            token = request.POST['token']
            request.session['token'] = token
        if token is None and request.session['token'] is not None:
            token = request.session['token']
        if token is not None:
            token1 = Token.objects.get(key=token)
            return render(request, "admin/studentlisting.html", {})
        else:
                if request.session.get('token', False):
                    del request.session['token']
                return redirect("index")
            
def teachers(request):
    with transaction.atomic():
        token = None
        if 'token' in request.POST.keys():
            token = request.POST['token']
            request.session['token'] = token
        if token is None and request.session['token'] is not None:
            token = request.session['token']
        if token is not None:
            token1 = Token.objects.get(key=token)
            user = token1.user
            checkGroup1 = user.is_superuser
            checkGroup2 = user.groups.filter(name='student').exists()
            if checkGroup1:
                return render(request, "admin/teacherlisting.html", {})
            else:
                return render(request, "student/teacherlisting.html", {})
        else:
                if request.session.get('token', False):
                    del request.session['token']
                return redirect("index")
            
            
def addteacher(request):
    return render(request, "admin/addteacher.html", {})

def teachertimeslots(request):
    return render(request, "teacher/slotlisting.html", {})



def logout(request):
    with transaction.atomic():
        token = None
        try:
            if request.session.get('token', False):
                del request.session['token']
            return redirect("index")
        except:
            token = None
            return render(request, "login.html",)