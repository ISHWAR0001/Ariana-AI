import os
import subprocess
import time
from command import *  
from chat import *

# Remove DISPLAY variable if it exists (avoiding KeyError)
os.environ.pop("DISPLAY", None)
    
# Get environment variables for the current environment
env_vars = os.environ.copy()

# Start the Flask server from db.py using subprocess
flask_process = subprocess.Popen(["python", "db.py"])

# Wait for a few seconds to ensure the Flask server has started
time.sleep(1)  # adjust this sleep time depending on server's startup time

# Play sound after opening the UI
ClickOnMicSound()

# Now open the UI in the browser (Flask UI on localhost:5000)
os.system('start msedge "http://127.0.0.1:5000"') 