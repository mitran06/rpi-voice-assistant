import google.generativeai as genai
import os
import speech_recognition as sr
import time
from dotenv import load_dotenv
from elevenlabs import play
from elevenlabs.client import ElevenLabs

# Load API keys from .env
load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


# Configure Gemini AI
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 200, 
    },
    system_instruction="You are a helpful voice assistant. Answer concisely and naturally, without lists, formatting, or structured prompts.",
)

def speak(text):
    """Generate and play voice using ElevenLabs"""
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Replace with the correct voice_id for 'Rachel'
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)



def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio).lower()
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Speech recognition is unavailable.")
            return None
        except sr.WaitTimeoutError:
            return None

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that")
        except sr.RequestError:
            speak("Speech recognition service is unavailable")
        except sr.WaitTimeoutError:
            speak("No input detected")
    
    return None

def ask_ai(prompt):
    response = model.generate_content(prompt)
    return response.text 

while True:
    wake_word = listen()
    if wake_word and "computer" in wake_word.lower():
        print("Wake word detected")
        speak("Yes, how can I help you?")
        
        last_response_time = time.time()

        while True:
            command = listen_for_command()
            if command:
                if "be quiet" in command or "shut up" in command:
                    continue  # Stop responding but keep listening

                print("You:", command)
                ai_response = ask_ai(command)
                print("AI:", ai_response)
                speak(ai_response)
                last_response_time = time.time()

            if time.time() - last_response_time > 7:
                print("No response for 7 seconds. Going back to wake word mode.")
                break
