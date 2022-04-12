from django.db import models


class Department(models.Model):
    deptName = models.CharField(max_length=255, null=True)
    section = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.deptName+"-"+self.section
class Teacher(models.Model):
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Attendence(models.Model):
    Teacher_user_id = models.CharField(max_length=255,null=True)
    Student_department = models.CharField(max_length=5,null=True)
    section = models.CharField(max_length=1, null=True)
    period = models.IntegerField()
    Date   = models.CharField(max_length=10)

    def __str__(self):
        return str(self.Teacher_user_id)

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
    def __str__(self) -> str:
        return self.reg





    



