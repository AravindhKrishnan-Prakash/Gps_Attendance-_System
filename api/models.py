from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return f"{self.username} - {self.role}"

class StaffAttendance(models.Model):
    staff_name = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)
    classroom = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    generated_code = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.staff_name} - {self.generated_code}"
class StudentAttendance(models.Model):
    student_name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=50)
    staff_name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    location = models.JSONField()
    code = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.subject_code} - {self.student_name}"

class AttendanceRecord(models.Model):
    staff_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    attendance_status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Doubt', 'Doubt')])
    code_validation = models.CharField(max_length=100)
    location_validation= models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.student_name} - {self.course_code} - {self.attendance_status}'