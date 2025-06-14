from django.conf import settings
from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # e.g., 'CS101'
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    credits = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.id} - {self.title}'

class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.email} in {self.course.id} Grade: {self.grade or "N/A"}'

class ScheduleEvent(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='schedule_events')
    event = models.CharField(max_length=200, blank=True)  # for non-course events like 'Study Group for PHY210'
    location = models.CharField(max_length=200)

    def __str__(self):
        if self.course:
            return f'{self.day} {self.time.strftime("%I:%M %p")} - {self.course.id} @ {self.location}'
        else:
            return f'{self.day} {self.time.strftime("%I:%M %p")} - {self.event} @ {self.location}'

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Not Started')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Medium')

    def __str__(self):
        return f'{self.title} ({self.course.id}) - Due {self.due_date}'

class Notification(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.student.email}: {self.message[:30]}...'

class Resource(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.title