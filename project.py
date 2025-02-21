#instalar a biblioteca gTTS !pip install gTTS

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from gtts import gTTS
import os
import pyjokes
import wikipedia
import webbrowser
from pygame import mixer
from datetime import datetime
import playsound

# Função para capturar áudio do microfone
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You said: " + said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available.")
    return said.lower()

# Função para converter texto em fala
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "/content/voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

# Função para responder aos comandos
def respond(text):
    print("Text from get audio: " + text)
    if 'youtube' in text:
        speak("What do you want to search for?")
        keyword = get_audio()
        if keyword != '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.open(url)
            speak(f"Here is what I have found for {keyword} on youtube.")
    elif 'search' in text:
        speak("What do you want to search for?")
        query = get_audio()
        if query != '':
            result = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia,")
            print(result)
            speak(result)
    elif 'joke' in text:
        speak(pyjokes.get_joke())
    elif 'what time' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        speak(f"The current time is {strTime}")
    elif 'play music' in text or 'play song' in text:
        speak("Now playing...")
        music_dir = "/content/music/"  # Ajuste para seu diretório de música
        songs = os.listdir(music_dir)
        print(songs)
        playmusic(music_dir + "/" + songs[0])
    elif 'stop music' in text:
        speak("Stopping playback.")
        stopmusic()
    elif 'exit' in text:
        speak("Goodbye, till next time.")
        exit()

# Função para tocar música
def playmusic(song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()

# Função para parar música
def stopmusic():
    mixer.music.stop()

# Função para ativar o reconhecimento de fala quando o botão é clicado
def start_listening():
    speak("Listening...")
    text = get_audio()
    if text != "":
        respond(text)

# Função para o botão de comando de texto
def start_text_command():
    command = entry.get()
    if command != "":
        respond(command)

# Criando a janela principal
root = tk.Tk()
root.title("Assistente Virtual")
root.geometry("400x300")

# Mensagem inicial
label = tk.Label(root, text="Bem-vindo à Assistente Virtual!", font=("Arial", 14))
label.pack(pady=20)

# Botão para ativar o reconhecimento de voz
voice_button = tk.Button(root, text="Escutar Comando de Voz", command=start_listening, font=("Arial", 12), width=20)
voice_button.pack(pady=10)

# Caixa de entrada para comandos de texto
entry_label = tk.Label(root, text="Ou digite seu comando:", font=("Arial", 12))
entry_label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=5)

# Botão para ativar comandos de texto
text_button = tk.Button(root, text="Executar Comando de Texto", command=start_text_command, font=("Arial", 12), width=20)
text_button.pack(pady=10)

# Botão para fechar a assistente
exit_button = tk.Button(root, text="Fechar Assistente", command=root.quit, font=("Arial", 12), width=20)
exit_button.pack(pady=20)

# Rodar a interface
root.mainloop()
