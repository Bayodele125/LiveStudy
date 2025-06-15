from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from collections import defaultdict
from django.db import models
from django.contrib import messages
from .models import Enrollment, ScheduleEvent, Task, Notification, Resource
from Account.models import InstructorProfile

def home(request):
    """
    Render the home page.
    """
    return render(request, 'home.html')

@login_required
def dashboard_view(request):
    student = request.user  # CustomUser instance

    enrollments = Enrollment.objects.select_related('course').filter(student=student)
    courses = [{
        'id': e.course.id,
        'title': e.course.title,
        'instructor': e.course.instructor,
        'credits': e.course.credits,
        'grade': e.grade,
    } for e in enrollments]

    student_courses_ids = enrollments.values_list('course__id', flat=True)
    events = ScheduleEvent.objects.filter(
        models.Q(course__id__in=student_courses_ids) | models.Q(course__isnull=True)
    ).order_by('day', 'time')

    DAYS_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = defaultdict(list)
    for event in events:
        schedule[event.day].append({
            'time': event.time.strftime('%I:%M %p'),
            'course': event.course.id if event.course else None,
            'event': event.event if not event.course else None,
            'location': event.location,
        })
    for day in DAYS_ORDER:
        if day not in schedule:
            schedule[day] = []

    tasks_qs = Task.objects.filter(student=student).select_related('course').order_by('due_date')
    tasks = [{
        'id': task.id,
        'title': task.title,
        'course': task.course.id,
        'due_date': task.due_date.isoformat(),
        'status': task.status,
        'priority': task.priority,
    } for task in tasks_qs]

    notifications_qs = Notification.objects.filter(student=student).order_by('-timestamp')[:10]
    from django.utils.timesince import timesince
    current_time = now()
    notifications = [{
        'id': note.id,
        'message': note.message,
        'timestamp': f"{timesince(note.timestamp, current_time)} ago",
        'read': note.read,
    } for note in notifications_qs]

    resources_qs = Resource.objects.all()
    resources = [{'title': r.title, 'url': r.url} for r in resources_qs]

    context = {
        'student': {
            'name': student.name,
            'student_id': student.student_id,
            'major': student.major,
            'year': student.year,
            'profile_picture_url': student.profile_picture_url or 'https://placehold.co/150x150/E0E0E0/333?text=NA',
            'email': student.email,
        },
        'courses': courses,
        'schedule': schedule,
        'tasks': tasks,
        'notifications': notifications,
        'resources': resources,
    }
    return render(request, 'home.html', context)



@login_required
def InstructorDashboard(request):
    """
    View for the instructor dashboard.
    """
    if not request.user.is_instructor:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    instructor = InstructorProfile.objects.get(user=request.user)

    context = {
        'instructor': instructor,
        'courses': instructor.courses.all(),
    }
    return render(request, 'instructor_dashboard.html', context)


