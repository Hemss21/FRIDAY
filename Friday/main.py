import os
import eel
import server

from engine.features import *
from engine.command import *
from engine.database import verify_login, create_user, check_session, get_current_user

eel.init("www")
playAssistantSound()

# Expose database functions to frontend
eel.expose(verify_login)
eel.expose(create_user)
eel.expose(check_session)
eel.expose(get_current_user)

os.system('start chrome.exe --app="http://localhost:8000/login.html"')
 
eel.start('login.html', mode=None, host='localhost', port=8000)