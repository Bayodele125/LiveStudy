import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from Account.models import InstructorProfile
from django.contrib.auth.decorators import login_required

def videocall(request, instructor_id=None):
    roomID = uuid.uuid4()

    # Find the instructor you want to notify
    try:
        instructor = InstructorProfile.objects.get(id=instructor_id) 
    except InstructorProfile.DoesNotExist:
        instructor = None

    # Send WebSocket notification
    if instructor:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instructor.id}",
            {
                'type': 'send_notification',
                'message': f"{request.user.username} has created a video room: {roomID}"
            }
        )

    context = {
        'roomID': roomID,
        'userID': request.user.user_id,
        'name': request.user.name,
        'appID': settings.APPID,
        'serverSecret': settings.SERVERSECRET,
    }
    return render(request, 'videocall.html', context)

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.name, 'userID': request.user.user_id})

@login_required
def videocall(request):
    roomID = uuid.uuid4()
    context = {
        'roomID': roomID,  # Generate a unique room ID,
        'userID': request.user.user_id,  # Pass the user ID to the template
        'name': request.user.name,
        'appID': settings.APPID,  # Pass the APPID from settings
        'serverSecret': settings.SERVERSECRET,  # Pass the SERVERSECRET from settings
    }
    return render(request, 'videocall.html', context)


@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')