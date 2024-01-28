import pyttsx3
from pypdf import PdfReader
from pydub import AudioSegment
from pathlib import Path
import os


file = open("demo.pdf", 'rb')
pdf_reader = PdfReader(file)
num_pages = len(pdf_reader.pages)
print(num_pages)

# Initalization of the Pyttsx3 engine
engine = pyttsx3.init()

#Set the prefered voice and rate
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[7].id)
engine.setProperty('rate', rate-5)
data = []
for num in range(0, num_pages):
    page = pdf_reader.pages[num]
    data.append(page.extract_text())
    # play.say('This is the converstion of pdf file to audio')
    # engine.say(data[num])
    engine.save_to_file(data[num], f"./audio_segments/{file.name[:-4]}_{num + 1}.mp3")
    # play.save_to_file('Hello World', 'test.mp3')
    engine.runAndWait()

#Saving each page to a different audio segment
p = Path('./audio_segments')

#Importing the separate Audio files from audio_segements
audio_files = [mp3_file for mp3_file in p.glob(f"{file.name[:-4]}*.mp3")]
#Sorting the audio files with creation date to avoid mis match
audio_files.sort(key=os.path.getmtime)
# audio_segments = [AudioSegment.from_file(mp3_file) for mp3_file in p.glob(f"{file.name[:-4]}*.mp3")]
audio_segments = [AudioSegment.from_file(audio_file) for audio_file in audio_files]
first_seg = audio_segments.pop(0)

#Appending different audio segments into one file
playlist = first_seg
for seg in audio_segments:

    playlist = playlist.append(seg)
    playlist_length = len(playlist) / (1000 * 60)

# lets save it with the length of file in minutes!
with open(f"{file.name[:-4]}.mp3", 'wb') as out_f:
    playlist.export(out_f, format='mp3')


