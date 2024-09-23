from django.contrib import admin
from .models import User,StaffAttendance,StudentAttendance,AttendanceRecord

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')

admin.site.register(StaffAttendance)
admin.site.register(StudentAttendance)
admin.site.register(AttendanceRecord)