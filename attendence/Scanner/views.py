from base64 import urlsafe_b64encode
from unicodedata import name
from urllib import request
import webbrowser
import cv2
import pyzbar
from pyzbar.pyzbar import decode
from django.db.models import Q

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
from.tokens import account_activation_token
from django.utils import timezone
from user_app.models import *
from user_app.models import TakingAttendence


def home(request):
    dip_list=[]
    for i in Department.objects.all():
        dip_list.append(i.deptName)

    context1={'obj':dip_list}
    #period=[1, 2, 3, 4, 5, 6, 7, 8]
    section=['-','A','B','C','D']
    #return render(request,'take_attendence.html',{'teacher':context,'department':context1,'period':period,'section':section})
    return render(request,'Scanner/index.html',{'department':context1,'section':section})
def signup(request):
    dip_list=[]
    for i in Department.objects.all():
        dip_list.append(i.deptName)

    context1={'obj':dip_list}
    #period=[1, 2, 3, 4, 5, 6, 7, 8]
    section=['-','A','B','C','D']
    if request.method =="POST":
        
        #return render(request,'take_attendence.html',{'teacher':context,'department':context1,'period':period,'section':section})
        #return render(request,'Scanner/index.html',{'department':context1,'section':section})
        username=request.POST.get("username",False)
        email= request.POST.get('emailid',False)
        pass1 =request.POST.get('pass1',False)
        pass2 = request.POST.get("pass2",False)
        dept1 =request.POST.get("dept",False)
        sec =request.POST.get("section",False)
                #messages.success(request,"your are successfully logined")
        if(pass1 == pass2):
            if Student.objects.filter(user_name=username).exists():
                messages.info(request,"username already exists")
                return redirect("signup")
                
            elif Student.objects.filter(emailid= email).exists():
                messages.info(request,"Email already exists")
                return redirect('signup')
            else:

                myuser = Student.objects.create(user_name=username,emailid=email,password =pass1,department=dept1,section=sec)
                myuser.is_active=False
                #myuser1=myuser
                myuser.save()
                    #return redirect('signin') 
                    #return redirect('signin')     
                        
                            #Student.objects.create(myuser.cleaned_data)
                            
                        #return HttpResponse(request,"created")
                        
                    #elif(Student.objects.filter(user_name=username).exists()==False):
                        #myuser = Student.objects.create(user_name=username,emailid=email,password =pass1)
                        #myuser.save()              
                    
                            #Student.objects.create(myuser.cleaned_data)
                        #return redirect('signin')
                        

                #return HttpResponse(request,"created")
                #welcome email
                sub="welcome to Qr_attendence webpage"
                msg="Hello"+myuser.user_name+"!! \n"+"welocme to qr_attendence !! \n Thank ypu for visiting our website \n we have snet you confirmation mail ,please confirm your email to activate your Account .\n\n Thanking you \n Fantastic #4"
                from_email = settings.EMAIL_HOST_USER
                to_list =[myuser.emailid]
                send_mail(sub,msg,from_email,to_list,fail_silently=True)
                #sending an email link
                current_site = get_current_site(request)
                email_subject = "Confirm your Email @ Qr-attendence  Login!!"
                message2 = render_to_string('Scanner/email_confirmation.html',{
                    
                    'name': myuser.user_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_b64encode(force_bytes(myuser.pk)),
                    'token': account_activation_token.make_token(myuser)
                })
                email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.emailid],
                )
                email.fail_silently = True
                email.send()
                return redirect('signin') 
        else:
            messages.info(request,"password not match")
            return redirect('signup')
    #return render(request,'Scanner/signup.html')
    return render(request,'Scanner/signup.html',{'department':context1,'section':section})

            #else:
            #messages.info(request,"not rendering")
        
    
def signin(request):
    """if request.method=='POST':
        email=request.POST.get("emailid")
        password1= request.POST.get("pass")
        user = authenticate(emailid=email,password=password1)
        if user is not None:
            login(request,user)
            username1=user.emailid
            messages.info(request,"succesfully logged in ")
            return redirect("signin")
        else:
            messages.info(request,"invalid credentials!" )
            return redirect("signin")
    else:
        messages.info(request,"not redirect")
        #return redirect("signin")
    return render(request,'Scanner/signin.html')"""
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
               print(i.emailid)

        if(Email in Student_dir and Student_dir[Email]==password):
            #messages.info(request,"Successfullyloggedin")
            return redirect("scanner")

            #return render(request,'take_attendence.html',context)
        else:
            messages.info(request,"Invalid password or Email Id")
            return redirect("signin")




    return render(request,'Scanner/signin.html')


"""def signout(request):
    pass"""
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = Student.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Student.DoesNotExist):
        myuser=Student.objects.get(pk=uid)

    if myuser is not None:
         return render(request,'Scanner/activation_failed.html')
        
    else:
        #messages.info(request,myuser)
       
        #myuser.is_active = True
        #user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.info(request, "Your Account has been activated!!")
        return redirect('signin')
# Create your views here.
def scanner(request):
    return render(request,"Scanner/Scanner_pg1.html")
def index(request):
    return render(request, 'Scanner/home.html')
def gen(camera):
    while True:
        frame= camera.get_frame()
        
        s,var=camera.get().read()
        #decodedObjects = decode(var)
        detector = cv2.QRCodeDetector()
    
        

        if detector is not None:
            for code in  decode(var):
                camera.getuse().append(code.data.decode('utf-8'))
                if code.data.decode('utf-8') in camera.getuse():
                    
                    #myuser=Attendence.objects.create(qrinfo=code.data.decode('utf-8'))
                    #myuser.save()
                    webbrowser.open(str(code.data.decode('utf-8')))
                    #return HttpResponse("successfully scanned")
                    #messages.info(request,{{code.data.decode('utf-8')}})
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
    """else:
        return redirect("signin")"""
def link(request,date):

        per=date[8]
        dat=date[0:4]+"-"+date[4:6]+"-"+date[6:8]
        stu_sec=date[14:]
        stu_dep=date[9:14].replace("_","")
        e = str(a['obj'])
        con1={'date':dat,'period':per}

        si = Student.objects.filter(Q(section__in = [stu_sec])&Q(department__in=[stu_dep]))

        l = list(si)
        
        
        for i in l:
            if str(TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= [i])& Q(section__in=[stu_sec]))) not in list(TakingAttendence.objects.all()):
                TakingAttendence.objects.create(date=dat, reg =i, deapartment_name=stu_dep, section=stu_sec, period_1="A",period_2="A", period_3="A", period_4="A", period_5="A", period_6="A", period_7="A", period_8="A")


        l2 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= [e])& Q(section__in=[stu_sec]))
        
        l3 = list(l2)
        
        if per == "1":
            for i in l3:
                i.period_1 = "P"
                i.save()
            abs1 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_1__in=["A"]))
        if per == "2":
            for i in l3:
                i.period_2 = "P"
                i.save()
            abs2 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_2__in=["A"]))
        if per == "3":
            for i in l3:
                i.period_3 = "P"
                i.save()
            abs3 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_3__in=["A"]))
        if per=="4":
            print('period-4')
            for i in l3:
                i.period_4 = "P"
                print('mahesh')
                i.save()
            abs4 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_4__in=["A"]))
        if per=="5":
            for i in l3:
                i.period_5 = "P"
                i.save()
            abs5 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_5__in=["A"]))
        if per=="6":
            for i in l3:
                i.period_6 = "P"
                i.save()
            abs6 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_6__in=["A"]))
        if per=="7":
            for i in l3:
                i.period_7 = "P"
                i.save()
            abs7 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_7__in=["A"]))
        if per=="8":
            for i in l3:
                i.period_8 = "P"
                i.save()
            abs8 = TakingAttendence.objects.filter(Q(date__in = [dat])& Q(deapartment_name__in =[stu_dep])&Q(reg__in= e)& Q(section__in=[stu_sec]) & Q(period_8__in=["A"]))


    
        return render(request,"Scanner/link.html",{"abc":a,"b":con1,"c":con1})
    
        #return HttpResponse("login first")






