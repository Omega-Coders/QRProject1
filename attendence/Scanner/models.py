from django.db import models

# Create your models here.
class Student(models.Model):
    user_name = models.CharField(max_length=30)
    emailid = models.CharField(max_length=30)
    password =models.CharField(max_length=30)
class Attendence(models.Model):
    qrinfo = models.CharField(max_length=200)

class Teacher(models.Model):
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email



class StudentDetail(models.Model):
    regno = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    section = models.CharField(max_length=1)

    def __str__(self):
        return self.regno

class TakingAttendence(models.Model):
    date = models.CharField(max_length=255)
    reg = models.CharField(max_length=255)
    deapartment_name = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    period_1 = models.CharField(max_length=255)
    period_2 = models.CharField(max_length=255)
    period_3 = models.CharField(max_length=255)
    period_4 = models.CharField(max_length=255)
    period_5 = models.CharField(max_length=255)
    period_6 = models.CharField(max_length=255)
    period_7 = models.CharField(max_length=255)
    period_8 = models.CharField(max_length=255)
    

