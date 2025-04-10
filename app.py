import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "config", ".env"))

from src.listener import listen, listen_for_command
from src.speaker import speak, stop_speak
from src.ai_engine import ask_ai
from src.spotify import play_song
from config.settings import settings
import time

try:
    while True:
        wake_word = listen()
        if wake_word and settings["sr"]["wake_word"] in wake_word:
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
                        print("You:", command)
                        song = command[5:].strip()
                        if not play_song(song):
                            speak("I couldn't find that song.")
                        break

                    print("You:", command)
                    ai_response = ask_ai(command)
                    print("AI:", ai_response)
                    speak(ai_response)
                    last_response_time = time.time()

                if time.time() - last_response_time > settings["sr"]["command_timeout"]:
                    print("No response for a while. Listening for wake word again.")
                    break
except KeyboardInterrupt:
    print("Exiting...")
    stop_speak()
    exit(0)