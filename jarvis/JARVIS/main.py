import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from datetime import datetime, timedelta

r = sr.Recognizer()
engine = pyttsx3.init()
nasaapi = "LBFM3Rtr9BdRQGommKopAK63v0JLdMwQ9BxSb8Nr"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(c):
    c = c.lower()

    if "open chat" in c:
        webbrowser.open("https://chatgpt.com/")
    elif "open google" in c:
        webbrowser.open("https://google.com/")
    elif "open game" in c:
        webbrowser.open("https://cardgames.io/chess/")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com/")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com/")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com/")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "geomagnetic storm" in c:
        start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = datetime.today().strftime('%Y-%m-%d')
        url = f"https://api.nasa.gov/DONKI/GST?startDate={start_date}&endDate={end_date}&api_key={nasaapi}"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                if data:
                    for storm in data:
                        speak(f"Storm detected on {storm.get('startTime', 'unknown date')}")
                else:
                    speak("No geomagnetic storms detected in the past week.")
            else:
                speak("NASA API request failed.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")

def listen_for_wake_word():
    print("Listening for 'Jarvis'...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)
            return "jarvis" in word.lower()
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            print("Didn't catch that.")
            return False
        except Exception as e:
            print(f"Recognition error: {e}")
            return False

def listen_for_command():
    print("Listening for command...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=5)
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
            return None
        except Exception as e:
            speak(f"Error occurred: {str(e)}")
            return None

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        if listen_for_wake_word():
            speak("Yes?")
            command = listen_for_command()
            if command:
                process_command(command)