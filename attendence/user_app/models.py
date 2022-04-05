from django.db import models


class Department(models.Model):
    deptName = models.CharField(max_length=255, null=True)
    section = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.deptName
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

    def __str__(self):
        return str(self.Teacher_user_id)

    




