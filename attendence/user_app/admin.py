from django.contrib import admin


from .models import Teacher, Department, Attendence, StudentDetail, TakingAttendence

class TakingAttendenceAdmin(admin.ModelAdmin):
    list_display = ['date', 'reg', 'deapartment_name', 'section','period_1', 'period_2', 'period_3','period_4', 'period_5', 'period_6', 'period_7', 'period_8']

# class StudentDetailAdmin(admin.ModelAdmin):
#     list_display = ['regno', 'department', 'section']

class AttendenceAdmin(admin.ModelAdmin):
    list_display = ['Date', 'Teacher_user_id', 'Student_department', 'section', 'period']

admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Attendence, AttendenceAdmin)
admin.site.register(StudentDetail)
admin.site.register(TakingAttendence, TakingAttendenceAdmin)
