from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import InstructorProfile, StudentProfile
from django.contrib import messages
import uuid

def split_email(email):
    """
    Splits an email address into username and domain.
    """
    if '@' not in email:
        raise ValueError("Invalid email format")
    
    username, domain = email.split('@')
    return domain

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.is_active = True
            is_instructor = split_email(email) == 'instructor.com'
            if is_instructor:
                user.is_instructor = True  # Custom field to identify instructors
                user.user_id='INS/' + str(uuid.uuid4()),  # Generate a unique ID for the instructor profile

                # Create an instructor profile
                InstructorProfile.objects.create(
                    user=user
                )
            else:
                # Create a student profile
                user.is_student = True  # Custom field to identify students
                user.user_id='STU/' + str(uuid.uuid4()),  # Generate a unique ID for the student profile
                StudentProfile.objects.create(
                    user=user
                )
            user.save()
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')  
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            if user.is_student:
                return redirect('student_dashboard')
            elif user.is_instructor:
                return redirect('instructor_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')