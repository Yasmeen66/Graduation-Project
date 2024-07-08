import threading
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
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


#recorder = VoiceRecorder()


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == 'POST':
        # form = CustomUserForm(request.POST)
        # if form.is_valid():
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')

        print(f"exist?? {CustomUser.objects.filter(email=email).exists()}")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User already exists. Please log in.')
            return redirect('signup')
        else:
            hashed_password = make_password(password)
            user=CustomUser(
                name=name,
                email=email,
                phone=phone,
                password=hashed_password,
            )
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')

    else:
      #form = CustomUserForm()
      print("GET")
    return render(request, 'SignUp.html')


def login(request):
    print(f"login---{request.method}")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"email = {email}------- password = {password}")


        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'SignIn.html')

        elif not (CustomUser.objects.filter(email=email).exists()):
                messages.error(request, 'User does not exist. Please register first.')
                return render(request, 'SignIn.html')

        user = authenticate(request, email=email, password=password)
        print(f"user in login {user}")
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('new_meeting'))
        else:
            messages.error(request, 'Invalid email or password.')

            return render(request, 'SignIn.html')
    return render(request, 'SignIn.html')


@login_required
def new_meeting(request):
    global recorderInstance
    if request.method == "POST":
        meeting_name = request.POST.get('meeting_name')
        email = request.POST.get('email')
        recorderInstance = RecordEntry(meeting_name=meeting_name, email=email)
        return redirect('record_voice')
    return render(request, 'NewMeeting.html')


@login_required
@csrf_exempt
def record_voice(request):
    global recorders, recorderInstance
    if request.method == "POST":
        user = request.user
        print(user)

        if user not in recorders:
            recorders[user] = VoiceRecorder(recorderInstance)

        recorder = recorders[user]

        action = request.POST.get('action')
        status = "Invalid action"

        if action == 'start':
            if not recorder.recording:
                threading.Thread(target=recorder.start_recording).start()
                status = "Recording started"
            else:
                status = "Already recording"
        elif action == 'stop':
            if recorder.recording:
                recorder.stop_recording()
                del recorders[user]
                status = "Recording stopped"
            else:
                status = "Not currently recording"

        return JsonResponse({"Status": status})

    return render(request, 'record.html')


@login_required
def show_data(request):
    record_entries = RecordEntry.objects.filter(email=request.user.email)
    if request.method == 'POST':
        selected_option = request.POST.get('inlineRadioOptions')
        selected_meeting = request.POST.get('selectedMeeting')
        if selected_option == 'summarize' and selected_meeting:
            return redirect('show_summary', meeting_name=selected_meeting)
    context = {
        'record_entries': record_entries,
    }
    return render(request, 'LastMeeting.html', context)


@login_required
def show_summary(request, meeting_name):
    try:
        record_entry = RecordEntry.objects.get(email=request.user.email, meeting_name=meeting_name)
        summary = record_entry.summary
    except RecordEntry.DoesNotExist:
        summary = "No summary found for this meeting."

    context = {
        'summary': summary,
    }

    return render(request, 'summary.html', context)
