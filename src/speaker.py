import os, pygame, time
from elevenlabs.client import ElevenLabs
from config.settings import settings
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def speak(text):
    # stop mixer
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    # remove old files
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

    audio_data = client.text_to_speech.convert(
        text=text,
        voice_id=settings["elevenlabs"]["voice_id"],
        model_id=settings["elevenlabs"]["model_id"],
        output_format="mp3_44100_128",
    )
    # save audio
    with open("temp_audio.mp3", "wb") as f:
        f.write(b"".join(audio_data))

    # init mixer
    pygame.mixer.init()
    pygame.mixer.music.load("temp_audio.mp3")
    time.sleep(0.2) # delay for buffering
    pygame.mixer.music.play()

def stop_speak():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
