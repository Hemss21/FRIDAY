import pyttsx3
import speech_recognition as sr
import eel
import time
from .features import openCommand, playYoutube, chat_with_llama  # Add chat_with_llama import
import webbrowser


@eel.expose
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        time.sleep(2)
            
    except Exception:
        return ""

    return query.lower()

@eel.expose
def allCommands():
    query = takecommand()
    if query:
        if "open" in query.lower():
            openCommand(query)
            eel.redirectToMain()
        elif "play" in query.lower():
            playYoutube(query)
            eel.redirectToMain()
        else:
            # Use Llama for all other queries
            response = chat_with_llama(query)
            eel.DisplayMessage(response)
            speak(response)  # Add this line to speak the response
            eel.redirectToMain()
    else:
        print("Speak clearly")
        speak("Speak clearly")
        eel.redirectToMain()
    
        