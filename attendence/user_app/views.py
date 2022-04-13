from django.http import HttpResponse
from base64 import urlsafe_b64encode
import qrcode
from django.core.mail import EmailMessage
#from pyqrcode import QRCode
from django.http import FileResponse
#from sympy import rcode
from Scanner.models import *
from attendence import settings
from django.contrib.sites.shortcuts import get_current_site
from .models import Teacher, Department,Attendence, TakingAttendence
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from Scanner.models import Student
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from Scanner.tokens import *

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def register1(request):
    
    return render(request, "reg_form.html")

def login1(request):
    return render(request,'login.html')

def register(request):

    if request.method=='POST':
        global email
        email=request.POST['Email']
        b= email.find("@")
        username=email[:b]
        global departmentt
        departmentt=request.POST.get("dept",False)
        global password1
        password1=request.POST['Password']
        conform_pass=request.POST['Conform password']
        if(password1 == conform_pass):
            
                     
            if Teacher.objects.filter(email= email).exists():
                messages.info(request,"Email already exists")
                return redirect('register')
            else:
                #myuser = Student.objects.create(user_name=username,emailid=email,password =pass1,department=dept1,section=sec)
                #myuser.is_active=False
                #myuser.save()
                # sending an eamil msg to clent 
                sub="welcome to Qr_attendence webpage"
                msg="Hello"+" "+username+"!! \n"+"welocme to qr_attendence !! \n Thank you for visiting our website \n we have sent you confirmation mail ,please confirm your email to activate your Account .\n\n Thanking you \n Fantastic #4"
                from_email = settings.EMAIL_HOST_USER
                to_list =[email]
                send_mail(sub,msg,from_email,to_list,fail_silently=True)
                #sending an email link
                current_site = get_current_site(request)
                email_subject = "Confirm your Email @ Qr-attendence  Login!!"
                message2 = render_to_string('email_confirmation1.html',{
                    'name': username,
                    'domain': current_site.domain,
                    'uid':  urlsafe_base64_encode(force_bytes(email)),
                    'token': generate_token .make_token(email)
                })
                email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [email],
                )
                email.fail_silently = True
                email.send()
                return redirect('signin') 
        else:
            messages.info(request,"password not match")
            return redirect('register')
    return render(request,'reg_form.html')
def activate1(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        username1=None
        print(uid)
        if  uid is not None:   
            username1 = uid
            print(username1)
    except (TypeError,ValueError,OverflowError,Student.DoesNotExist):
        username1 = None
    try:
        if username1 is not None and generate_token.check_token(username1,token):
            #username1.is_active = True
            myuser=Teacher.objects.create(email=username1,password=password1, department=departmentt)
            messages.info(request, "Your Account has been activated!!")
            return redirect('signin')
        else:
            return render(request,'Scanner/activation_failed.html')
    except:
        return HttpResponse("link already expired")
    return HttpResponse("link already expired")
    """if(password1==conform_pass):
            
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
        return HttpResponse("mfnfnf")"""


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
        date=request.POST['date']

        si = Student.objects.filter(Q(section__in = [stu_sec])&Q(department__in=[stu_dep]))
        l = list(si)
        for i in l:
            if len(TakingAttendence.objects.filter(Q(date__in = [date])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= [i])& Q(section__in=[stu_sec]))) <1:
                TakingAttendence.objects.create(date=date, reg =i, deapartment_name=stu_dep, section=stu_sec, period_1="A",period_2="A", period_3="A", period_4="A", period_5="A", period_6="A", period_7="A", period_8="A")
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


    lis = list(abs)
    d = {}
    for i in range(len(lis)):
        d[i] = str(lis[i])

    return render(request, 'abs.html', context={'absent': d})



""""
def get_qr(response,temp):
    strr=os.path.join(str(BASE_DIR)+"\\attendence\\All_QR_codes"+("\\"+str(temp)+".png"))

    img = open(strr, 'rb')
    print(strr)

    response = FileResponse(img)

    return response
"""    

    


        

