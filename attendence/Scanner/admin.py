from django.contrib import admin
from .models import Student,Attendence

class StudentAdmin(admin.ModelAdmin):
    list_display = ['emailid', 'department', 'section']

admin.site.register(Student, StudentAdmin)
admin.site.register(Attendence)



# Register your models here.
