import re
import subprocess
from playsound import playsound
import eel
from .config import ASSISTANT_NAME
import os
import webbrowser
import pywhatkit as kit
import requests
import json

@eel.expose
def chat_with_llama(query):
    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"
    
    # Request payload
    data = {
        "model": "llama2",
        "prompt": query,
        "stream": False
    }
    
    try:
        # Generate response
        response = requests.post(url, json=data)
        response_json = response.json()
        
        if 'response' in response_json:
            return response_json['response']
        else:
            return "I apologize, but I couldn't process your request at the moment."
    except Exception as e:
        return "Sorry, there was an error processing your request."

def playAssistantSound():
    music_dir = "www/assets/audio/sound.mp3"
    playsound(music_dir)

@eel.expose
def openCommand(query):
    from .command import speak  # Import here to avoid circular dependency
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()

    if query!="":
        speak("Opening "+query)
        os.system("start "+query)
    else:
        speak("Not found")

@eel.expose
def playYoutube(query):
    from .command import speak  # Import here to avoid circular dependency
    search_term = extract_yt_term(query)
    speak("Playing "+ search_term+" on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(query):
    pattern = r'play\s+(.*?)\s+on\s+YouTube'
    match = re.search(pattern, query, re.IGNORECASE)  # Changed 'command' to 'query'
    if match:
        return match.group(1)
    return query.replace("play", "").strip()  # Fallback if pattern doesn't match


@eel.expose
def google_sign_in(user_data):
    try:
        from .database import create_user
        # Create user with Google sign-in data
        result = create_user(
            first_name=user_data.get('firstName', ''),
            last_name=user_data.get('lastName', ''),
            username=user_data.get('email', ''),
            password=None  # Google users don't need a password
        )
        return {
            "status": True,
            "first_name": user_data.get('firstName', '')
        }
    except Exception as e:
        return {"status": False, "message": str(e)}