import threading
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .VoiceRecorder import VoiceRecorder
from .forms import CustomUserForm
from .models import CustomUser
from django.urls import reverse
from django.contrib import messages

recorder = VoiceRecorder()


def home(request):
    return render(request,"home.html")


def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
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
    return render(request, 'NewMeeting.html')


@csrf_exempt
def record_voice(request):
    global recorder
    if request.method == "POST":
        if recorder.recording:
            recorder.recording = False
            status = "Recording stopped"
        else:
            recorder = VoiceRecorder()
            threading.Thread(target=recorder.click_handler).start()
            status = "Recording started"
        return JsonResponse({"Status": status})
    return render(request, 'home.html')
