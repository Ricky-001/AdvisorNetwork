from django.shortcuts import render
from django.http import *
import json
from .models import Advisor, User, Bookings
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views

def home(request):
    return render(request,'index.html')

def AdminHome(request):
    return render(request,'admin.html')

def UserHome(request):
    return render(request,'user.html')

def AddAdvisor(request):

    if request.method == 'POST':
        advname = request.POST['aname']
        imgurl = request.POST['img']

        if advname == '' or imgurl == '':
            #return render(request, 'addadv.html', {'message':'400_BADREQUEST'})
            return HttpResponseBadRequest(status=400)
        
        Advisor.objects.create(advName=advname,imgURL=imgurl).save()
        
        #return render(request, 'addadv.html', {'message':'200_OK'})
        return HttpResponse(status=200)
    else:
        return render(request,'addadv.html')

def UserRegister(request):

    if request.method == 'POST':
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        pwd = request.POST['pwd']

        if uname == '' or uemail == '' or pwd == '':            
            return HttpResponseBadRequest(status=400)

        elif User.objects.filter(uEmail=uemail).exists():
            return render(request, 'register.html', {'message':'Email Exists'})

        else:            
            User.objects.create(uName=uname,uEmail=uemail,password=pwd).save()
            
            if User.objects.filter(uEmail=uemail,password=pwd).exists():
                user = User.objects.get(uEmail=uemail)
                token = Token.objects.create(user=user)

                authKEY = token.key
                authUID = token.user.id
                cont = {'Token' : authKEY, 'User ID' : authUID}
                cont = json.dumps(cont)
                return HttpResponse(content=cont, status=200)
            else:
                return HttpResponse('Unauthorised',status=401)        
    else:
        return render(request,'register.html')

def UserLogin(request):
    if request.method == 'POST':
        uemail = request.POST['uemail']
        pwd = request.POST['pwd']

        if uemail == '' or pwd == '':            
            return HttpResponseBadRequest(status=400)

        else:                        
            if User.objects.filter(uEmail=uemail,password=pwd).exists():
                
                authuser = User.objects.get(uEmail=uemail)                
                try:
                    token = Token.objects.get(user=authuser)
                except:
                    token = Token.objects.create(user=authuser)
                
                authKEY = token.key
                authUID = token.user.id
                cont = {'Token' : authKEY, 'User ID' : authUID}
                cont = json.dumps(cont)
                return HttpResponse(content=cont, status=200)
            else:
                return HttpResponse('Unauthorised',status=401)
    else:
        return render(request,'login.html')

def AuthUser(request,uid):
    try:
        if User.objects.get(id=uid) and Token.objects.get(user=User.objects.get(id=uid)):
            return render(request,'authuser.html')
        else:        
            return HttpResponseNotFound('User does not exist',status=404)
    except User.DoesNotExist:
        return HttpResponseNotFound('User does not exist',status=404)

def ViewAll(request,uid):
    advisors = Advisor.objects.all()
    return render(request,'viewall.html', {'advisors':advisors})

def BookAdvisor(request,uid,aid):
    try:
        if Advisor.objects.get(id=aid):
            usr = User.objects.get(id=uid)
            adv = Advisor.objects.get(id=aid)
            if request.method == 'POST':
                booktime = request.POST['book_time']
                Bookings.objects.create(uID=usr,aID=adv,time=booktime).save()
                return HttpResponse(status=200)
            else:
                return render(request,'book.html', {'adv':adv})
        else:
            return HttpResponseNotFound('User does not exist',status=404)
    except User.DoesNotExist:
        return HttpResponseNotFound('User does not exist',status=404)

def ViewBookings(request,uid):
    try:
        if Bookings.objects.filter(uID=uid):
            bookings = Bookings.objects.filter(uID=uid)
            return render(request,'bookings.html', {'schedule':bookings})
        else:
            return HttpResponseNotFound('User does not exist',status=404)
    except User.DoesNotExist:
        return HttpResponseNotFound('User does not exist',status=404)
