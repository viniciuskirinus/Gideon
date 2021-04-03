#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json
import core
from nlu.classifier import classify

# Síntese de fala
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-2].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def evaluate(text):
    # Reconhecer entidade de texto.
    entity = classify(text)
    if entity == 'time|getTime':
        speak(core.SystemInfo.get_time())
    elif entity == 'time|getDate':
        speak(core.SystemInfo.get_date())

    # Abrir programas
    elif entity == 'open|notepad':
        speak('Abrindo o bloco de notas')
        os.system('notepad.exe')
    elif entity == 'open|opera':
        speak('Abrindo o Opera')
        os.system('"C:/Users/vinic/AppData/Local/Programs/Opera GX/launcher.exe"')

    print('Text: {} Entity: {}'.format(text, entity))

# Reconhecimento de fala

model = Model('model')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Loop do reconhecimento de fala

while True:
    data = stream.read(8192, exception_on_overflow=False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)

        if result is not None:
            text = result['text']
            evaluate(text)

            

        
