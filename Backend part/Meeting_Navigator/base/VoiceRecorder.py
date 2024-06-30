import os
import wave
import threading
import pyaudio
import speech_recognition as sr
from .models import RecordEntry

class VoiceRecorder:
    def __init__(self):
        self.recording = False

    def click_handler(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        while self.recording:
            try:
                data = stream.read(1024)
                frames.append(data)
            except IOError as e:
                print(f"Error recording: {e}")
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a .wav file
        sound_file_path = self.save_audio(frames)

        # Perform speech recognition on the recorded audio
        if sound_file_path:
            recognized_text = self.recognize_speech(sound_file_path)
            if recognized_text:
                # Save recognized text to database
                record_entry = RecordEntry(content=recognized_text)
                record_entry.save()

                # Save recognized text to a text file
                text_file_path = os.path.splitext(sound_file_path)[0] + ".txt"
                with open(text_file_path, "w") as text_file:
                    text_file.write(recognized_text)

                print(f"Text saved to database and text file: {text_file_path}")

    def save_audio(self, frames):
        exists = True
        i = 1
        while exists:
            if os.path.exists(f"recording{i}.wav"):
                i += 1
            else:
                exists = False

        sound_file_path = f"recording{i}.wav"
        sound_file = wave.open(sound_file_path, "wb")
        sound_file.setnchannels(1)
        sound_file.setframerate(44100)
        sound_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

        return sound_file_path

    def recognize_speech(self, audio_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            try:
                print("Processing audio file:", audio_file_path)
                audio_data = recognizer.record(source)
                recognized_text = recognizer.recognize_google(audio_data, language='en-US')
                print(f"Recognized text: {recognized_text}")
                return recognized_text
            except sr.UnknownValueError as e:
                print(f"Speech Recognition could not understand audio: {e}")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service: {e}")

        return None
