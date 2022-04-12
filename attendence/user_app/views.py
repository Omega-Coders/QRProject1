from django.http import HttpResponse
import qrcode
#from pyqrcode import QRCode
from django.http import FileResponse
#from sympy import rcode
from Scanner.models import *
from .models import Teacher, Department,Attendence, TakingAttendence
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from .models import Teacher, Department,Attendence

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent


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
            section=['A','B','C','D']
            return render(request,'take_attendence.html',{'abc':context,'department':context1,'period':period,'section':section})
        else:
            return HttpResponse("Invalid password or Email Id")

    else:
        return HttpResponse("fail")
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
def generate_qr(request):
    if request.method=='POST':
        user_name=request.POST.get('UserName')
        global stu_dep, stu_sec, period, date
        stu_dep=request.POST['dept']
        stu_sec=request.POST['section']
        period=request.POST['period']
        date=request.POST.get('date')
        stu_depp=stu_dep
        if(len(stu_dep)==5):
            stu_depp=stu_dep
        else:
            while(len(stu_depp)<5):
                stu_depp+="_"
        s = "http://127.0.0.1:8000/link/"+str(date).replace("-","")+""+str(period)+stu_depp+stu_sec
        img = qrcode.make(s)
        user=Attendence.objects.create(Teacher_user_id=user_name,Student_department=stu_dep, section=stu_sec,period=period,Date=date)
        #fname="Qr_img.png"
        img.save(str(BASE_DIR)+"/attendence/static/Qr_img.png",scale=6)
        """
        strr=os.path.join(str(BASE_DIR)+"//attendence"+("//"+str(fname)))
        img = open(strr, 'rb')
    
        response = FileResponse(img)
        """  

        

        
            
        return render(request,"img.html")
    else:
        print("error---enjoy")
        return HttpResponse("error---enjoy")

st=1
def stop_qr(request):
    try:

        os.remove(str(BASE_DIR)+"\\attendence\\static\\Qr_img.png")
    except:
        os.remove(str(BASE_DIR)+"//attendence//static//Qr_img.png")

    
    global st
    st=0
    
    if period == '1':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_1__in=["A"]))
    if period == '2':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_2__in=["A"]))
    if period == '3':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_3__in=["A"]))
    if period == '4':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_4__in=["A"]))
    if period == '5':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_5__in=["A"]))
    if period == '6':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_6__in=["A"]))
    if period == '7':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_7__in=["A"]))
    if period == '8':
        abs = TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])& Q(section__in=[stu_sec]) & Q(period_8__in=["A"]))


    
    return HttpResponse(abs)



""""
def get_qr(response,temp):
    strr=os.path.join(str(BASE_DIR)+"\\attendence\\All_QR_codes"+("\\"+str(temp)+".png"))

    img = open(strr, 'rb')
    print(strr)

    response = FileResponse(img)

    return response
"""    

    


        

