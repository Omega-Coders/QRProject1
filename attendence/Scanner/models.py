from django.db import models

# Create your models here.
class Student(models.Model):
    user_name = models.CharField(max_length=30)
    emailid = models.CharField(max_length=30)
    password =models.CharField(max_length=30)
    department = models.CharField(max_length=255, default="")
    section = models.CharField(max_length=1, default="")
    def __str__(self):
        return self.emailid
class Attendence(models.Model):
    qrinfo = models.CharField(max_length=200)





    

    


    

