
from django.shortcuts import render
from django.http import HttpResponse
from .models import Teacher, Department, Attendence

def register1(request):
    return render(request, "home.html")

def register(request):

    if request.method=='POST':
        Email=request.POST['Email']
        departmentt=request.POST['dept']
        password1=request.POST['Password']
        conform_pass=request.POST['Conform password']
        
        if(password1==conform_pass):
            
            if Teacher.objects.filter(email = Email).exists():
                return HttpResponse(request,"Email already exists")
            else:
                user=Teacher.objects.create(email=Email,password=password1, department=departmentt)
                user.save()
                return HttpResponse(request,"created")
        else:
            return HttpResponse(request,"password not match")

    else:
        return HttpResponse(request,"mfnfnf")
