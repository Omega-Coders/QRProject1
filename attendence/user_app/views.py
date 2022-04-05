
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Teacher, Department, Attendence

def register1(request):
    return render(request, "reg_form.html")

def login1(request):
    return render(request,'login.html')

def register(request):

    if request.method=='POST':
        Email=request.POST['Email']
        departmentt=request.POST['dept']
        password1=request.POST['Password']
        conform_pass=request.POST['Conform password']
        
        if(password1==conform_pass):
            
            if Teacher.objects.filter(email = Email).exists():
                return HttpResponse("Email already exists")
            else:
                user=Teacher.objects.create(email=Email,password=password1, department=departmentt)
                user.save()
                print("teacher created")
                return render(request,"login.html")
        else:
            return HttpResponse("password not match")

    else:
        return HttpResponse("mfnfnf")


def login(request):
    if request.method=='POST':
        Email=request.POST['Email']
        password=request.POST['password']
    
        Teacher_dir={}

        for i in Teacher.objects.all():
           Teacher_dir[i.email]=i.password
           if(i.email==Email):
               context={'obj':i}

        if(Email in Teacher_dir and Teacher_dir[Email]==password):
            dip_list=[]
            for i in Department.objects.all():
                dip_list.append(i.deptName)

            context1={'obj':dip_list}
            period=[1, 2, 3, 4, 5, 6, 7, 8]
            section=['-','A','B','C','D']
            return render(request,'take_attendence.html',{'teacher':context,'department':context1,'period':period,'section':section})
        else:
            return HttpResponse("Invalid password or Email Id")

    else:
        return HttpResponse("fail")
        

def generate_qr(request):
    if request.method=='POST':
        user_name=request.POST.get('UserName')
        stu_dep=request.POST['dept']
        stu_sec=request.POST['section']
        period=request.POST['period']

        user=Attendence.objects.create(Teacher_user_id=user_name,Student_department=stu_dep, section=stu_sec,period=period)
        user.save()
        print("Qrcode created")
        return HttpResponse("Attendence object created")

    else:
        print("error---enjoy")
        return HttpResponse("error---enjoy")





        

