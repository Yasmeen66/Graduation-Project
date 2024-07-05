import os
import threading
import time
import wave
import pyaudio
import whisper  # Replace with your actual transcription library or method

from base.models import RecordEntry


class VoiceRecorder:
    def __init__(self, user, meeting_name, meeting_subject):
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        self.user = user
        self.meeting_name = meeting_name
        self.meeting_subject = meeting_subject

    def start_recording(self):
        self.recording = True
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                                      frames_per_buffer=1024)
        self.frames = []
        threading.Thread(target=self.record).start()

    def record(self):
        start = time.time()
        while self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)
            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            # Update recording time here if needed

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        audio_file_path = self.save_audio()
        if audio_file_path:
            self.transcribe_audio(audio_file_path)

    def save_audio(self):
        i = 1
        while os.path.exists(f"recording{i}.wav"):
            i += 1

        audio_file_path = f"recording{i}.wav"
        sound_file = wave.open(audio_file_path, "wb")
        sound_file.setnchannels(1)
        sound_file.setframerate(44100)
        sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        sound_file.writeframes(b"".join(self.frames))
        sound_file.close()

        print(f"Audio saved as: {audio_file_path}")
        return audio_file_path

    def transcribe_audio(self, audio_file):
        try:
            model = whisper.load_model("base")  # Example usage of hypothetical whisper library
            result = model.transcribe(audio_file, fp16=False)

            output_text_file = os.path.splitext(audio_file)[0] + ".txt"
            with open(output_text_file, "w", encoding='utf-8') as f:  # Specify encoding here
                f.write(result["text"])
            transcription_text = result["text"]

            # Save transcription text to RecordEntry model
            print(f"Transcription saved to: {output_text_file}")
            record_entry = RecordEntry(
                content=transcription_text,
                user=self.user,
                meeting_name=self.meeting_name,
                meeting_subject=self.meeting_subject
            )
            record_entry.save()
            return output_text_file

        except Exception as e:
            print(f"Error occurred during transcription: {e}")
            return None
