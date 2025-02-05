import os
import subprocess
import time
from command import *  # Assuming you have some functions in the command module
from chat import *      # Assuming you have some functions in the chat module

# Start the Flask server from db.py using subprocess
flask_process = subprocess.Popen(["python", "db.py"])

# Wait for a few seconds to ensure the Flask server has started
time.sleep(1)  # You can adjust this sleep time depending on your server's startup time

# Now open the UI in the browser (Flask UI on localhost:5000)
os.system('start msedge "http://127.0.0.1:5000"')

# Optional: Play sound or run other code after opening the UI
ClickOnMicSound()  # Assuming this function is defined in command or chat modules

# If you want to block further execution and keep the UI open, you can add more code here, or it will run in the background.
