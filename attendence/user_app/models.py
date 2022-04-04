from django.db import models


class Department(models.Model):
    deptName = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.deptName
class Teacher(models.Model):
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Attendence(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=1, null=True)
    period = models.IntegerField()

    




