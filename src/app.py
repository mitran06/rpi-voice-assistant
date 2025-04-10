import os
import json
import time
import pygame
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from spotify import play_song

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

config_path = os.path.join(os.path.dirname(__file__), "../config/settings.json")
with open(config_path, "r") as f:
    settings = json.load(f)


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={
        "temperature": settings["genai"]["temperature"],
        "max_output_tokens": settings["genai"]["max_output_tokens"],
    },
    system_instruction=settings["genai"]["instruction"],
)

def speak(text):
    """Generate and play voice using ElevenLabs"""
    # stop mixer
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    # remove old files
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

    audio_data_generator = client.text_to_speech.convert(
        text=text,
        voice_id=settings["elevenlabs"]["voice_id"],
        model_id=settings["elevenlabs"]["model_id"],
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio_data_generator)

    # save audio
    with open("temp_audio.mp3", "wb") as f:
        f.write(audio_bytes)

    # init mixer
    pygame.mixer.init()
    pygame.mixer.music.load("temp_audio.mp3")
    time.sleep(0.2)  # brief pause to not clip
    pygame.mixer.music.play()

def stop_speak():
    """Stop any ongoing speech."""
    if pygame.mixer.get_init() is not None:
        pygame.mixer.music.stop()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=settings["sr"]["timeout"])
            text = recognizer.recognize_google(audio).lower()
            return text
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
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
            print("Sorry, I didn't catch that")
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
    if wake_word and settings["sr"]["wake_word"] in (wake_word.lower() if wake_word else ""):
        print("Wake word detected")
        speak("Yes, how can I help you?")
        last_response_time = time.time()

        while True:
            command = listen_for_command()
            if command:
                # shut up
                if "be quiet" in command or "shut up" in command:
                    stop_speak()
                    continue
                # music
                if command.startswith("play "):
                    song_to_play = command[5:].strip()
                    success = play_song(song_to_play)
                    if not success:
                        speak("I couldn't find that song.")
                    break

                print("You:", command)
                ai_response = ask_ai(command)
                print("AI:", ai_response)
                speak(ai_response)
                last_response_time = time.time()

            if time.time() - last_response_time > settings["sr"]["command_timeout"]:
                print("No response for 7 seconds. Going back to wake word mode.")
                break
