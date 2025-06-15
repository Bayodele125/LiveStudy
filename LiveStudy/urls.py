"""
URL configuration for LiveStudy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core import views as core_views
from Account import views as account_views
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'instructors', account_views.InstructorViewSet)
# router.register(r'students', account_views.StudentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    path('meetings/', include('meeting.urls')),
    path('', core_views.home, name='home'),
    path('dashboard/', core_views.dashboard_view, name='student_dashboard'),
    path('instructor/dashboard/', core_views.InstructorDashboard, name='instructor_dashboard'),
    # path('courses/', core_views.courses_view, name='courses'),
    # path('courses/create/', core_views.create_course_view, name='create_course'),
    # path('courses/<int:course_id>/edit/', core_views.edit_course_view, name='edit_course'),
    # path('courses/<int:course_id>/', core_views.course_detail_view, name='course_detail'),
    # path('courses/<int:course_id>/enroll/', core_views.enroll_in_course, name='enroll_in_course'),
    # path('courses/<int:course_id>/unenroll/', core_views.unenroll_from_course, name='unenroll_from_course'),
    # path('courses/<int:course_id>/assignments/', core_views.assignments_view, name='assignments'),
    # path('courses/<int:course_id>/assignments/<int:assignment_id>/', core_views.assignment_detail_view, name='assignment_detail'),
    # path('courses/<int:course_id>/assignments/<int:assignment_id>/submit/', core_views.submit_assignment, name='submit_assignment'),
    # path('courses/<int:course_id>/assignments/<int:assignment_id>/grade/', core_views.grade_assignment, name='grade_assignment'),
    # path('courses/<int:course_id>/resources/', core_views.resources_view, name='resources'),
    # path('courses/<int:course_id>/resources/<int:resource_id>/', core_views.resource_detail_view, name='resource_detail'),
    # path('courses/<int:course_id>/resources/add/', core_views.add_resource_view, name='add_resource'),
    # path('courses/<int:course_id>/resources/<int:resource_id>/edit/', core_views.edit_resource_view, name='edit_resource'),
    # path('courses/<int:course_id>/resources/<int:resource_id>/delete/', core_views.delete_resource_view, name='delete_resource'),
    # path('courses/<int:course_id>/schedule/', core_views.schedule_view, name='schedule'),
    # path('courses/<int:course_id>/schedule/add/', core_views.add_schedule_event, name='add_schedule_event'),
    # path('courses/<int:course_id>/schedule/<int:event_id>/edit/', core_views.edit_schedule_event, name='edit_schedule_event'),
    # path('courses/<int:course_id>/schedule/<int:event_id>/delete/', core_views.delete_schedule_event, name='delete_schedule_event'),
    # path('courses/<int:course_id>/tasks/', core_views.tasks_view, name='tasks'),
    # path('courses/<int:course_id>/tasks/add/', core_views.add_task_view, name='add_task'),
    # path('courses/<int:course_id>/tasks/<int:task_id>/edit/', core_views.edit_task_view, name='edit_task'),
    # path('courses/<int:course_id>/tasks/<int:task_id>/delete/', core_views.delete_task_view, name='delete_task'),
    # path('courses/<int:course_id>/tasks/<int:task_id>/complete/', core_views.complete_task_view, name='complete_task'),
    # path('courses/<int:course_id>/tasks/<int:task_id>/incomplete/', core_views.incomplete_task_view, name='incomplete_task'),
    # path('courses/<int:course_id>/notifications/', core_views.notifications_view, name='notifications'),
    # path('courses/<int:course_id>/notifications/<int:notification_id>/mark_read/', core_views.mark_notification_read, name='mark_notification_read'),
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
