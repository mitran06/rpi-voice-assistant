import speech_recognition as sr
from config.settings import settings

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=settings["sr"]["timeout"])
            return recognizer.recognize_google(audio).lower()
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
            return None

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that")
        except sr.RequestError:
            from src.speaker import speak
            speak("Speech recognition service is unavailable")
        except sr.WaitTimeoutError:
            from src.speaker import speak
            speak("No input detected")
    return None
