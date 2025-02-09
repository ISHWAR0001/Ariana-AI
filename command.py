from playsound import playsound as ps
import pyttsx3
import speech_recognition as sr
import webbrowser
import time
import eel
import sys
import os
import google.generativeai as genai
from engine.auth import recognize
from engine.auth import sample
from engine.auth import trainer
import threading

API_KEY = os.getenv("Google_Gemini_API_Key")

# Ensure the API key is available
if API_KEY is None:
    raise ValueError("Google_Gemini_API_Key environment variable is not set.")

chatstr = ""
def chat(text):
    global chatstr
    genai.configure(api_key = API_KEY)
    chatstr += f"{text}\n"

    # Create the model
    generation_config = {
        "temperature": 0.5,
        "top_p": 0.85,
        "top_k": 40,
        "max_output_tokens": 200,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(chatstr)

    eel.DisplayMessage(response.text)
    speak(response.text)
    chatstr += f"{response.text}"
    return response

def ai(prompt):
    genai.configure(api_key = API_KEY)
    word = f"Ariana Response For Prompt: {''.join(prompt.split('intelligence')[1:]).strip()}\n **********************\n\n"

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(prompt)

    eel.DisplayMessage(response.text)
    speak("OK Sir")
    print(response.text)
    word += response.text
    
#playing sound function when we click on mic
@eel.expose
def ClickOnMicSound():
    music_dir = "static/assets/audio/start_sound.mp3"
    ps(music_dir)
    
#playing assistant sound function
@eel.expose
def playAssistantSound():
    speak("Welcome,In Ariana A.I. A Virtual Assistant")

@eel.expose
def takingFaceSamples():
    eel.showMessage("Starting Face Authentication")
    speak("Starting Face Authentication")
    time.sleep(5)
    eel.hideLoader()
    eel.showMessage("Collecting Face Data")
    speak("Collecting Face Data")
    sample.TakeFaceSample()
    
@eel.expose
def trainingFaceSamples():
    eel.hideFaceAuth2()
    eel.showMessage("Wait for few seconds")
    speak("Wait for few seconds")
    trainer.trainFaceSamples()
    eel.hideloadSpinner()
    eel.showMessage("Face Data Collected")
    speak("Face Data Collected")
    time.sleep(5)
    eel.hideSampleFace()

@eel.expose
def facialRecognition():
    eel.hideLoader()
    eel.showMessage("Ready For Face Authentication")
    speak("Ready For Face Authentication")
    flag = recognize.AuthenticateFace()
    if flag == 1 :
        eel.hideFaceAuth()
        eel.showMessage("Face Authentication Successfull")
        speak("Face Authentication Successfull")
        eel.hideFaceAuthSuccess()
        eel.showMessage("Hello, Ishwar")
        speak("Hello, Ishwar")
        playAssistantSound()
        eel.hideStart()
    else:
        eel.showMessage("Face Authentication Fail")
        speak("Face Authentication Fail")

#function which gives voice to assistant 
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) #for setting voice type
    engine.setProperty('rate', 174) #for setting voice speed
    engine.say(text)
    engine.runAndWait()  
    
#Taking query from users
def takecommand():
    # If stop_event is set, do not proceed further in this function
    if stop_event.is_set():
        return None  # Return empty string and avoid any further execution
    
    r = sr.Recognizer()

    #Directly import pyaudio if available
    try:
        import pyaudio
    except ImportError:
        print("pyAudio is required for microphone functionality")
        return None

    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
        print("Recognizing...")
        eel.DisplayMessage('Recognizing...')

        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said : {query}")
            return  query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that")
            return None
        except sr.RequestError:
            print("Speech Recognition service is unavailable")
            return None

running = False  # Global flag to control the main loop
stop_event = threading.Event()  # This event will be used to stop the function
    
@eel.expose
def back():
    global running
    stop_event.set()  # Set the event to stop the loop
    running = False  # Set this to False to stop the infinite loop in `main()`
    print("Back button clicked, stopping current process.")
    
#Function For Controlling And Processing All type of Work
@eel.expose    
def main():
    global running
    stop_event.clear()  # Clear the event to allow the loop to run again
    
    try:
        eel.DisplayMessage("Hello")
        speak("Hello")
        eel.DisplayMessage("How May I Help You?")
        speak("How May I Help You?")
        
        while True:
            print("Listening....")
            eel.DisplayMessage('Listening....')
            text = takecommand()
            eel.DisplayMessage(f"You : {text}")
            time.sleep(2)
        
            spell =''.join(text.split('open')[1:]).strip()
            sites = [[f'{spell}',f"https://{spell}.com"]]
        
            if f"Open {spell}".lower() in text.lower():
                for site in sites:
                    eel.DisplayMessage(f"Ariana : Opening {site[0]} sir...")
                    speak(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
                    exit()
                    eel.ShowHood()
            else:
                eel.DisplayMessage("Chatting...")
                chat(text)
    except :
        print("Error")
        

# Run the main function in a separate thread
@eel.expose
def run_main():
    global running
    if not running:  # Only start if running is False
        running = True  # Reset running flag before starting the main loop
        stop_event.clear()  # Clear the event to allow the main loop to run
        thread = threading.Thread(target=main)
        thread.daemon = True  # Ensures the thread terminates when the main program ends
        thread.start()
    else:
        print("Main function is already running.")
        
@eel.expose
def exitfacialrecognition():
    sys.exit(facialRecognition)
    
@eel.expose
def exitSampleFace():
    sys.exit(takingFaceSamples)
    sys.exit(sample.TakeFaceSample)
    