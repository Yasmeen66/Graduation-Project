# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member, RecordEntry
from .forms import MemberForm
from .VoiceRecorder import VoiceRecorder
import threading

recorder = VoiceRecorder()

def home(request):
    all_members = Member.objects.all()
    all_records = RecordEntry.objects.all()  # Retrieve all RecordEntry objects
    return render(request, 'home.html', {'all_members': all_members, 'all_records': all_records})

def register(request):
    if request.method == "POST":
        form = MemberForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'register.html', {'form': form})
    else:
        form = MemberForm()
        return render(request, 'register.html', {'form': form})

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
