import pyttsx3
import speech_recognition as sr
import AppOpener
import webbrowser
import openai
import os
import time
import pyautogui
import playsound

speaker = pyttsx3.init('sapi5')
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)
speaker.setProperty('rate', 150)


def ai(query):
    openai.api_key = os.getenv("OPEN_API_KEY")
    response = openai.Completion.create(model="text-davinci-003", prompt=query)
    return response['choices'][0]['text']


def listener():
    print('Listening....')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            # print(f"user said : {query}")
            return query
        except Exception:
            return "Some error occurred"


def speak(query):
    speaker.say(query)
    speaker.runAndWait()


def open_app(app):
    lists = AppOpener.give_appnames(upper=False)
    n = len(lists)
    count = 1
    for apps in lists:
        if apps in app:
            speak(f"Opening {app}")
            AppOpener.open(app,match_closest=True)
            break
        elif count >= n:
            speak("App not found")
            break
        count += 1


def open_web(website):
    webbrowser.open(f"https://www.{website}")
    speak(f"Opening {website}")


def close_app(app):
    AppOpener.close(app)


def shutdown():
    os.system("shutdown /s /t 5")


def play_music():
    speak("opening spotify")
    AppOpener.open("Spotify")
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    pyautogui.write('295',interval=0.1)
    for key in ['enter', 'tab', 'tab', 'tab', 'enter']:
        time.sleep(1)
        pyautogui.press(key)

def close(app):
    speak(f"Closing {app}")
    AppOpener.close(app)

def alexa():
    playsound.playsound('amazon_echo_show_wav.wav')
    action = listener()
    if "com".lower() in action.lower():
        print("com.....")
        open_web(action[5:])
    elif "play music".lower() in action.lower():
        print("music.....")
        play_music()
    elif "open".lower() in action.lower():
        print("opening.....",action[5:])
        open_app(action[5:].lower())
    elif "close".lower() in action.lower():
        print("closing",action[5:])
        close(action[5:])
    else:
        speak("Invalid action")

def google():
    playsound.playsound('amazon_echo_show_wav.wav')
    action = listener()
    speak(ai(action))      

while True:
    name = listener()
    if "alexa" in name.lower():
        alexa()
    elif "google" in name.lower():
        google()
        
            