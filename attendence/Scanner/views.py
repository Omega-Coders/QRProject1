from base64 import urlsafe_b64encode
import time
import os
from unicodedata import name
from urllib import request
import webbrowser
#from attendence.user_app import views
import cv2
import pyzbar
from pyzbar.pyzbar import decode
from django.db.models import Q
import user_app.views as xx
from distutils.log import info
#from email.message import EmailMessage
from django.core.mail import EmailMessage
#from . tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Attendence, Student
from django.contrib import messages
from django.contrib.auth import authenticate,login
from attendence import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
#from.tokens import account_activation_token
from django.utils import timezone
from user_app.models import *
from user_app.models import TakingAttendence
from .tokens import *
from user_app.views import *

def home(request):
    dip_list=[]
    for i in Department.objects.all():
        dip_list.append(i.deptName)
    context1={'obj':dip_list}
    section=['-','A','B','C','D']
    return render(request,'Scanner/welcome.html',{'department':context1,'section':section})
def signup(request):
    dip_list=[]
    for i in Department.objects.all():
        dip_list.append(i.deptName)
    context1={'obj':dip_list} 
    section=['A','B','C','D']
    if request.method =="POST":
        global username
        username=request.POST.get("username",False)
        global email
        
        email= request.POST.get('emailid',False)
        global email1
        email1=email
        global pass1
        pass1 =request.POST.get('pass1',False)
        pass2 = request.POST.get("pass2",False)
        global dept1
        dept1 =request.POST.get("dept",False)
        global sec
        sec =request.POST.get("section",False)
        if(pass1 == pass2):
            if Student.objects.filter(user_name=username).exists():
                messages.info(request,"username already exists")
                return redirect("signup")      
            elif Student.objects.filter(emailid= email).exists():
                messages.info(request,"Email already exists")
                return redirect('signup')
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
                message2 = render_to_string('Scanner/email_confirmation.html',{
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
            return redirect('signup')
    return render(request,'Scanner/signup.html',{'department':context1,'section':section})  
def signin(request):
    if request.method=='POST':
        Email=request.POST.get('emailid')
        password=request.POST.get('pass')
        Student_dir={}
        for i in Student.objects.all():
           Student_dir[i.emailid]=i.password
           if(i.emailid==Email):
               context={'obj':i}
               global a 
               a= context
               #print(i.emailid)
            
        if(Email in Student_dir and Student_dir[Email]==password):
            return redirect("scanner")
        if(Email not in Student_dir or Student_dir[Email]!=password ) :
            Teacher_dir={}
            for i in Teacher.objects.all():
                Teacher_dir[i.email]=i.password
                if(i.email==Email):
                    global email
                    context={'obj':i}
                    email =context
                    print(email)
            if(Email in Teacher_dir and Teacher_dir[Email]==password):
                dip_list=[]
                for i in Department.objects.all():
                    dip_list.append(i.deptName)

                context1={'obj':dip_list}
                period=[1, 2, 3, 4, 5, 6, 7, 8]
                section=['A','B','C','D']
                return render(request,'take_attendence.html',{'abc':context,'department':context1,'period':period,'section':section})
            else:
                messages.info(request,"Invalid password or Email Id")
            return redirect("signin")
        else:
            messages.info(request,"Invalid password or Email Id")
            return redirect("signin")
    return render(request,'Scanner/signin.html')


"""def signout(request):
    pass"""
def dir():
    directory="qr"
    parent_dir=os.path.abspath("//")
    print(parent_dir)
    path=os.path.join(parent_dir,directory)
    os.mkdir(path)


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        username1=None
        if  uid is not None:   
            username1 = uid
    except (TypeError,ValueError,OverflowError,Student.DoesNotExist):
        username1 = None
    try:

        if username1 is not None and generate_token.check_token(username1,token):
            #username1.is_active = True
    
            myuser = Student.objects.create(user_name=username,emailid=email1,password =pass1,department=dept1,section=sec)
        
          
            messages.info(request, "Your Account has been activated!!")
            return redirect('signin')
        else:
            return render(request,'Scanner/activation_failed.html')
    except:
        
        return HttpResponse("link already expired")
def scanner(request):
    return render(request,"Scanner/Scanner_pg1.html")
def index(request):
    return render(request, 'Scanner/home.html')
def gen(camera):
    while True:
        frame= camera.get_frame()
        s,var=camera.get().read()
        detector = cv2.QRCodeDetector()
        if detector is not None:
            for code in  decode(var):
                camera.getuse().append(code.data.decode('utf-8'))
                if code.data.decode('utf-8') in camera.getuse():
                    #dir()
                    webbrowser.open(str(code.data.decode('utf-8')))
                    time.sleep(5)
                else:
                    yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        """finally:
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')"""
def video_stream(request):
    dec=cv2.QRCodeDetector()
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')
def link(request,date):
    if(xx.st==0):
        return HttpResponse("QR Already expried")
    else:
        per=date[8]
        dat=date[0:4]+"-"+date[4:6]+"-"+date[6:8]
        stu_sec=date[14:]
        stu_dep=date[9:14].replace("_","")
        e = str(a['obj'])
        con1={'date':dat,'period':per}
        l2 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= [e])& Q(section__in=[stu_sec]))
        l3 = list(l2)
        if per == "1":
            for i in l3:
                i.period_1 = "P"
                i.save()
            abs1 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_1__in=["A"]))
            try:
                if(i.period_1 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")        
        if per == "2":
            for i in l3:
                i.period_2 = "P"
                i.save()
            abs2 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_2__in=["A"]))
            try:
                if(i.period_2 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        if per == "3":
            for i in l3:
                i.period_3 = "P"
                i.save()  
            abs3 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_3__in=["A"]))
            try:
                if(i.period_3 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        if per=="4":
            print('period-4')
            for i in l3:
                i.period_4 = "P"
                print('mahesh')
                i.save()
            abs4 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_4__in=["A"]))
            try:
                if(i.period_4 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        if per=="5":
            for i in l3:
                i.period_5 = "P"
                i.save()
            abs5 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_5__in=["A"]))
            try:
                if(i.period_5 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        if per=="6":
            for i in l3:
                i.period_6 = "P"
                i.save()
            abs6 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_6__in=["A"]))
            try:
                if(i.period_6 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        if per=="7":
            for i in l3:
                i.period_7 = "P"
                i.save()
            abs7 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_7__in=["A"]))
            try:
                if(i.period_7 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        if per=="8":
            for i in l3:
                i.period_8 = "P"
                i.save()
            abs8 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_8__in=["A"]))
            try:
                if(i.period_8 == "P"):
                    messages.info(request,"successfully taken")
            except:
                messages.info(request,"please try again")
        return render(request,"Scanner/link.html")

        #return HttpResponse("login first")






