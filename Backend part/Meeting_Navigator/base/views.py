import threading
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .record_and_transcript import VoiceRecorder
from .forms import CustomUserForm
from .models import CustomUser, RecordEntry
from django.urls import reverse
from django.contrib import messages
from .forms import RecordEntryForm

recorders = {}


def home(request):
    return render(request, "home.html")


def signup(request):

    if request.method == 'POST':

        form = CustomUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'User already exists. Please log in.')
                return redirect('login')
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = CustomUserForm()
    return render(request, 'SignUp.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting to authenticate user: {email} with password: {password}")

        try:
            user = CustomUser.objects.get(email=email)
            print(f"User found: {user.email}")
        except CustomUser.DoesNotExist:
            print(f"No user found with email: {email}")
            return render(request, 'SignIn.html', {'error': 'User does not exist. Please register first.'})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            print("User authenticated and logged in")
            return redirect(reverse('new_meeting'))
        else:
            print("Authentication failed")
            return render(request, 'SignIn.html', {'error': 'Invalid email or password'})
    else:
        print("Not a POST request")
    return render(request, 'SignIn.html')


@login_required
def new_meeting(request):
    if request.method == "POST":
        print("////////////////////////////////")
        form = RecordEntryForm(request.POST)
        if form.is_valid():
            print("*************************************form")
            meeting_name = form.cleaned_data['meeting_name']
            meeting_subject = form.cleaned_data['meeting_subject']
            # Store meeting name and subject in session
            request.session['meeting_name'] = meeting_name
            request.session['meeting_subject'] = meeting_subject
            form.save()
            return redirect('record_voice')
    else:
        form = RecordEntryForm()
    return render(request, 'NewMeeting.html', {'form': form})


@login_required
@csrf_exempt
@login_required
def record_voice(request):
    global recorders
    if request.method == "POST":
        user = request.user
        if user not in recorders:
            meeting_name = request.session.get('meeting_name')
            meeting_subject = request.session.get('meeting_subject')
            recorders[user] = VoiceRecorder(user=user, meeting_name=meeting_name, meeting_subject=meeting_subject)
        recorder = recorders[user]

        action = request.POST.get('action')
        if action == 'start':
            if not recorder.recording:
                threading.Thread(target=recorder.start_recording).start()
                status = "Recording started"
            else:
                status = "Already recording"
        elif action == 'stop':
            if recorder.recording:
                recorder.stop_recording()
                del recorders[user]  # Clean up the recorder instance
                status = "Recording stopped"
            else:
                status = "Not currently recording"
        else:
            status = "Invalid action"
        return JsonResponse({"Status": status})
    return JsonResponse({"Status": "Invalid request method"})
