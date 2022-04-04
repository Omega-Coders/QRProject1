
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
# Create your views here.
def register1(request):
    return render(request,'home.html')
def register(request):

    if request.method=='POST':
        Email=request.POST.get('Email')
        department=request.POST.get('Department')
        password1=request.POST.get('Password')
        conform_pass=request.POST.get('Conform password')
        
        if(password1==conform_pass):
            if User.objects.filter(username = Email).exists():
                print("username already exits")
            else:
                user=User.objects.create_user(username={Email},password=password1)
                user.save()
                print('user created')
        else:
            print("password not match")

    else:
        return HttpResponse(request,"mfnfnf")
