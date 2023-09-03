import os
import io
import PySimpleGUI as sg
import speech_recognition as sr
from pydub import AudioSegment


# Function to perform transcription
def transcribe_video(input_video_path):
    try:
        # Convert video to audio
        audio = AudioSegment.from_file(input_video_path, format="mp4")
        audio.export("temp_audio.wav", format="wav")

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load the audio file
        audio_file = "temp_audio.wav"
        with sr.AudioFile(audio_file) as source:
            print("Processing audio...")

            # Listen to the audio file using recognizer
            audio_data = recognizer.record(source)

            # Perform speech recognition
            text = recognizer.recognize_google(audio_data)
            return text

    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"


# Define the GUI layout
layout = [
    [sg.Text("Select an MP4 video to transcribe:*max 10MB")],
    [sg.Input(key="-FILE-", enable_events=True, size=(45, 1)), sg.FileBrowse()],
    [sg.Button("Transcribe")],
    [sg.Text("Transcription:", size=(40, 1))],
    [sg.Multiline(size=(40, 10), key="-TRANSCRIPT-", autoscroll=True)],
    [sg.Text("www.wshopcode.com", text_color="blue", enable_events=True, key="-WEBSITE-")],
]

# Create the window
window = sg.Window("Video Transcription App - wshopcode", layout)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Transcribe":
        video_path = values["-FILE-"]

        if not video_path:
            sg.popup_error("Please select an MP4 video file.")
        elif os.path.getsize(video_path) > 10 * 1024 * 1024:  # 10 MB limit
            sg.popup_error("File size exceeds 10 megabytes.")
        else:
            # Perform transcription
            transcription = transcribe_video(video_path)

            # Update transcript in the GUI
            window["-TRANSCRIPT-"].update(transcription)

    elif event == "-WEBSITE-":
        sg.popup("Visit our website at www.wshopcode.com")

# Close the window
window.close()
