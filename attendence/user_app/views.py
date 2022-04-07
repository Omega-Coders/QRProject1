from django.http import HttpResponse
import qrcode
from pyqrcode import QRCode
from django.http import FileResponse


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
            section=['-','A','B','C','D']
            return render(request,'take_attendence.html',{'teacher':context,'department':context1,'period':period,'section':section})
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
        stu_dep=request.POST['dept']
        stu_sec=request.POST['section']
        period=request.POST['period']

        

        date=request.POST['date']

        s = "http://127.0.0.1:8000/link/"+str(date).replace("-","")+""+str(period)
  
        
        img = qrcode.make(s)
  
       

        user=Attendence.objects.create(Teacher_user_id=user_name,Student_department=stu_dep, section=stu_sec,period=period,Date=date)
    
        fname="Qr_img.png"
        img.save(fname,scale=6)
        



        strr=os.path.join(str(BASE_DIR)+"\\attendence"+("\\"+str(fname)))

        img = open(strr, 'rb')
    
        response = FileResponse(img)
        print("Qrcode created")
        return response
        

    else:
        print("error---enjoy")
        return HttpResponse("error---enjoy")




""""
def get_qr(response,temp):
    strr=os.path.join(str(BASE_DIR)+"\\attendence\\All_QR_codes"+("\\"+str(temp)+".png"))

    img = open(strr, 'rb')
    print(strr)

    response = FileResponse(img)

    return response
"""    

    


        

