import os
import threading
import time
import wave
import pyaudio
import whisper  # Replace with your actual transcription library or method
from transformers import pipeline,set_seed
import tensorflow as tf
from haystack.nodes import QuestionGenerator
from base.models import RecordEntry

# Disable symlink warnings
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Specify the model and revision explicitly
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
# quiz_generator =QuestionGenerator(model_name_or_path="valhalla/t5-base-e2e-qg")




# report_generator = pipeline("Report ", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
# qa_generator = pipeline("Questions and Answers", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")


class VoiceRecorder:
    def __init__(self, recorderInstance):
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        self.recorderInstance = recorderInstance

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
            model = whisper.load_model("base")
            result = model.transcribe(audio_file, fp16=False)
            output_text_file = os.path.splitext(audio_file)[0] + ".txt"
            with open(output_text_file, "w", encoding='utf-8') as f:
                f.write(result["text"])
            transcription_text = result["text"]
            summary_text = VoiceRecorder.summarize_with_chatgpt(transcription_text)
            # quiz = VoiceRecorder.generate_quiz_questions(transcription_text)

            # report = VoiceRecorder.report_text(transcription_text)
            # Ques = VoiceRecorder.generate_questions(transcription_text)

            # Save transcription text to RecordEntry model
            print(f"Transcription saved to: {output_text_file}")
            print(f"Summary Text = {summary_text}")
            # print(f"Quiz = {quiz}")
            # print(f"report = {report}")
            # print(f"ques = {Ques}")



            record_entry = RecordEntry(
                meeting_name=self.recorderInstance.meeting_name,
                email=self.recorderInstance.email,
                content=transcription_text,
                summary=summary_text,
                # quiz=quiz,
                # report= report,
                # Ques = Ques,
            )
            record_entry.save()
            return output_text_file

        except Exception as e:
            print(f"Error occurred during transcription: {e}")
            return None

    def write_text_to_file(file_path, text):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Summary saved to '{file_path}'.")
        except OSError as e:
            print(f"Error writing to file: {e}")

    def summarize_with_chatgpt(transcription_text):
        if transcription_text:
            # Suppress TensorFlow warnings (optional)
            tf.get_logger().setLevel('ERROR')

            # Summarize the tra
            # nscription text
            summary = summarizer(transcription_text, max_length=100, min_length=30, do_sample=False)

            # Fixed output file path
            output_file_path = r"C:\Users\Yasmin\Desktop\output.txt"

            # Write summary to file
            VoiceRecorder.write_text_to_file(output_file_path, summary[0]['summary_text'])
            return summary[0]['summary_text']
        else:
            print("No transcription text provided to summarize.")

    # def generate_quiz_questions(transcription_text):
    #     if transcription_text:
    #         # Suppress TensorFlow warnings (optional)
    #         tf.get_logger().setLevel('ERROR')
    #
    #         # Generate quiz questions from the transcription text
    #         quiz_questions = quiz_generator.generate(transcription_text)
    #         print(f"quiz questions = {quiz_questions}")
    #
    #         # Fixed output file path
    #         output_file_path = r"C:\Users\Yasmin\Desktop\quiz_questions.txt"
    #
    #         # Write quiz questions to file
    #         VoiceRecorder.write_text_to_file(output_file_path, quiz_questions)
    #         return quiz_questions
    #     else:
    #         print("No transcription text provided to generate quiz questions.")

    # def report_text(transcription_text):
    #     if transcription_text:
    #         # Suppress TensorFlow warnings (optional)
    #         tf.get_logger().setLevel('ERROR')
    #
    #         # Summarize the transcription text
    #         summary = report_generator(transcription_text, max_length=150, min_length=30, do_sample=False)
    #
    #         # Fixed output file path
    #         output_file_path = r"C:\Users\Yasmin\Desktop\summary.txt"
    #
    #         # Write summary to file
    #         VoiceRecorder.write_text_to_file(output_file_path, summary[0]['summary_text'])
    #         return summary[0]['summary_text']
    #     else:
    #         print("No transcription text provided to summarize.")
    #
    # def generate_questions(transcription_text):
    #     if transcription_text:
    #         # Suppress TensorFlow warnings (optional)
    #         tf.get_logger().setLevel('ERROR')
    #
    #         # Generate QA output from the transcription text
    #         qa_output = qa_generator(transcription_text, max_new_tokens=50, do_sample=False)
    #
    #         # Fixed output file path
    #         output_file_path = r"C:\Users\Yasmin\Desktop\qa_output.txt"
    #
    #         # Write QA output to file
    #         VoiceRecorder.write_text_to_file(output_file_path, qa_output[0]['generated_text'])
    #
    #         return qa_output[0]['generated_text']
    #     else:
    #         print("No transcription text provided to generate QA output.")
    #
