
from skills.base_skill import BaseSkill
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

class SpotifySkill(BaseSkill):
    intent = "spotify"

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope="user-read-playback-state,user-modify-playback-state"
        ))

    def handle(self, text, player):
        text = text.lower()

        if "spotify" not in text:
            return False, None

        try:
            if "play" in text:
                query = text.replace("spotify", "").replace("play", "").strip()
                return True, self.play_track(query)

            elif "pause" in text:
                self.sp.pause_playback()
                return True, "Playback paused."

            elif "resume" in text:
                self.sp.start_playback()
                return True, "Playback resumed."

            elif "next" in text:
                self.sp.next_track()
                return True, "Skipping track."

            elif "previous" in text:
                self.sp.previous_track()
                return True, "Going back."

            elif "what is playing" in text:
                return True, self.current_track()

            else:
                return True, "Spotify command not recognized."

        except Exception as e:
            return True, f"Spotify error: {str(e)}"

    def play_track(self, query):
        result = self.sp.search(q=query, type="track", limit=1)
        if not result["tracks"]["items"]:
            return "Track not found."

        track = result["tracks"]["items"][0]
        track_uri = track["uri"]

        self.sp.start_playback(uris=[track_uri])

        return f"Playing {track['name']} by {track['artists'][0]['name']}"

    def current_track(self):
        current = self.sp.current_playback()
        if not current or not current.get("item"):
            return "Nothing is playing."

        track = current["item"]
        return f"Currently playing {track['name']} by {track['artists'][0]['name']}"
