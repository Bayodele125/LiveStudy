from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

import uuid  # For generating unique room names (optional)

def start_meeting(request):
    """
    Renders a template with the Jitsi Meet IFrame.
    """
    room_name = uuid.uuid4()  # Generate a unique room name (optional)
    context = {'room_name': room_name} #Pass room name to the template
    return render(request, 'room.html', context)  # Create meeting.html

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    context = {
        'roomID':uuid.uuid4(),  # Generate a unique room ID,
        'userID': request.user.id,  # Pass the user ID to the template
        'name': request.user.username,
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