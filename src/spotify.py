import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state user-modify-playback-state"
    ),
    requests_timeout=30
)

def play_song(song_name):
    print(f"Searching for song: {song_name}")
    result = sp.search(q=song_name, type='track', limit=1)
    tracks = result.get('tracks', {}).get('items', [])

    if not tracks:
        print("Song not found.")
        return False

    track = tracks[0]
    devices = sp.devices()
    device_id = devices["devices"][0]["id"]
    sp.start_playback(device_id=device_id, uris=[track['uri']])
    print(f"Playing: {track['name']} by {track['artists'][0]['name']}")
    return True
