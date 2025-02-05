import speech_recognition as sr
import win32com.client
import webbrowser
import datetime
import os
import google.generativeai as genai

speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatstr = ""
def chat(text):
    global chatstr
    # print(chatstr)
    genai.configure(api_key="AIzaSyABh2DLrMOweASZsDJfX_y8mZzYI2PcsxY")
    chatstr += f"Ishwar : {text}\n"

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
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(chatstr)

    # speaker.Speak("OK Sir")
    speaker.Speak(response.text)
    chatstr += f"{response.text}"
    return response

def ai(prompt):
    genai.configure(api_key="AIzaSyABh2DLrMOweASZsDJfX_y8mZzYI2PcsxY")
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
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(prompt)

    speaker.Speak("OK Sir")
    print(response.text)
    word += response.text

    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    with open(f"Gemini/{''.join(prompt.split('intelligence')[1:]).strip()}", "w") as f:
        f.write(word)

def takecommand():
    r = sr.Recognizer()

    #Directly import pyaudio if available
    try:
        import pyaudio
    except ImportError:
        print("pyAudio is required for microphone functionality")
        return None

    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        print("Recognizing...")

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

def help():
    print("Can I Help You in another way")
    speaker.Speak("Can I Help You in another way")

if __name__ == '__main__':
    speaker.Speak("Hello I am Ariana AI")
    speaker.Speak("How May I Help You?")
    while True:
        print("Listening....")
        text = takecommand()
        spell =''.join(text.split('open')[1:]).strip()
        print(spell)

        # sites = [["youtube","https://youtube.com"], ["google", "https://google.com"],["facebook", "https://facebook.com"],["instagram", "https://instagram.com"],["wikipedia", "https://wikipedia.com"],["twitter", "https://twitter.com"]]

        sites = [[f'{spell}',f"https://{spell}.com"]]
        # print(sites)

        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                help()

        if "the time" in text:
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"the time is {strftime}")
            speaker.Speak(f"The time is {strftime}")
            help()

        elif "Using Artificial Intelligence".lower() in text.lower():
            ai(prompt=text)
            help()

        elif "yes".lower() in text.lower():
            print("Sure, How May I Help You?")
            speaker.Speak("Sure, How May I Help You?")

        elif "No".lower() in text.lower():
            speaker.Speak("Ok,Welcome Sir")
            exit()

        else:
            print("Chatting.....")
            chat(text)
