from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, StaffAttendance, StudentAttendance
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer 
from .models import AttendanceRecord
from rest_framework.views import APIView
from urllib.parse import unquote

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Generate token or session here if needed
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def staff(request):
    if request.method == 'POST':
        staff_name = request.data.get('staff_name')
        batch = request.data.get('batch')
        classroom = request.data.get('classroom')
        subject = request.data.get('subject')
        generated_code = request.data.get('generated_code')

        # Create and save the attendance record
        attendance = StaffAttendance(
            staff_name=staff_name,
            batch=batch,
            classroom=classroom,
            subject=subject,
            generated_code=generated_code
        )
        attendance.save()

        return Response({"message": "Attendance data saved successfully"})
@api_view(['POST'])
def store_student_data(request):
    # Extract data from request
    if request.method == 'POST':
        student_name = request.data.get('studentName')
        roll_number = request.data.get('rollNumber')
        staff_name = request.data.get('staffName')
        subject_code = request.data.get('subjectCode')
        status = request.data.get('status')
        location = request.data.get('location')
        code = request.data.get('code')

        # Create a new StudentAttendance entry
        attendance = StudentAttendance(
            student_name=student_name,
            roll_number=roll_number,
            staff_name=staff_name,
            subject_code=subject_code,
            status=status,
            location=location,
            code=code
        )
        attendance.save()
        return Response({"message": "Attendance recorded successfully!"})

@api_view(['POST'])
def record_attendance(request):
    # Extracting data from request
    date = request.data.get('date')
    staff_name = request.data.get('staff_name')
    subject = request.data.get('subject')


    Location={"GRDLAB":{"Latitude":11,"Longitude":77},}
    #  "PROGRAMMINGLAB1", "PROGRAMMINGLAB2", "HARDWARELAB"

    # Fetching matching records
    student_attendances = StudentAttendance.objects.filter(date=date, subject_code=subject)
    staff_attendances = StaffAttendance.objects.filter(date=date, staff_name=staff_name)

    code1="Failed"
    result="Absent"
    # Loop through records to create AttendanceRecords
    for student in student_attendances:
        for staff in staff_attendances:

            if staff.subject == subject and staff.staff_name == staff_name:
                if student.code == staff.generated_code:
                    code1="Pass"
                    if student.status =="Present":
                        result="Present"
                if student.status == "Absent":
                    result="Absent"
                if student.status == "Present" and student.code != staff.generated_code:
                    result="Doubt"


                # Create AttendanceRecord
                AttendanceRecord.objects.create(
                    staff_name=staff.staff_name,
                    student_name=student.student_name,
                    roll_number=student.roll_number,
                    course_code=student.subject_code,
                    attendance_status=result,
                    code_validation=code1,
                    date=date
                )
            code1="Failed"
    
    return Response({"message": "Attendance records updated successfully!"})
@api_view(['POST'])
def view_attendance(request):
    staff_name = request.data.get('staff_name')
    subject_code = request.data.get('subject_code')
    date = request.data.get('date')

    # Filter AttendanceRecord matching staff_name, subject_code, and date
    records = AttendanceRecord.objects.filter(staff_name=staff_name, course_code=subject_code, date=date)
    result = [
        {
            'student_name': record.student_name,
            'roll_number': record.roll_number,
            'course_code': record.course_code,
            'attendance_status': record.attendance_status,
            'code_validation': record.code_validation,
            'date': record.date
        }
        for record in records
    ]
    return Response(result)