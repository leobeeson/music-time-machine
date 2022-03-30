import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from typing import List

from song_metadata_curator import SongMetadataCurator

from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDERICT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-modify-private"


class SpotifyClient():

    def __init__(self) -> None:
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDERICT_URI
        self.authenticate(SCOPE)
        self.get_access_token()
        self.create_spotipy_object()
        self.get_user_id()

  
    def authenticate(self, scope) -> SpotifyOAuth:      
        oauth_manager = SpotifyOAuth(
                client_id = self.client_id,
                client_secret = self.client_secret,
                redirect_uri = self.redirect_uri,
                scope = scope,
                show_dialog = True,
                cache_path= "token.txt"
            )
        self.oauth_manager = oauth_manager


    def get_access_token(self) -> None:
        self.oauth_manager.get_access_token(as_dict = False)


    def create_spotipy_object(self) -> None:
        self.spotify = Spotify(auth_manager = self.oauth_manager)


    def get_user_id(self) -> None:
        user_profile = self.spotify.current_user()
        user_id = user_profile["id"]
        self.user_id = user_id


    def get_all_spotify_song_ids(self, songs: List[dict]) -> List[dict]:
        metadata_curator = SongMetadataCurator()
        songs_with_uris = []
        for song in songs:
            song_title = song["song_title"]
            song_title = metadata_curator.remove_apostrophes(song_title) 
            artist_name = song["artist_name"]
            artist_name = metadata_curator.normalise_singer_collaboration(artist_name) 
            track_uris = self.get_spotify_song_id(song_title, artist_name)
            song_with_uris = {
                "song_title": song_title,
                "artist_name": artist_name,
                "track_uris":  track_uris
            }
            songs_with_uris.append(song_with_uris)
        return songs_with_uris

    
    def get_spotify_song_id(self, song_title: str, artist_name: str) -> List[str]:
        track_uris = []
        response = self.spotify.search(q = f"track:{song_title} artist:{artist_name}", type = "track")
        try:
            items = response["tracks"]["items"]
            if len(items) > 0:
                for item in items:
                    try:
                        track_uri = item["uri"]
                        track_uris.append(track_uri)
                    except KeyError:
                        print(f"NO SPOTIFY URI: {song_title} by {artist_name}.")
        except KeyError:
            print(f"TRACK NOT FOUND: {song_title} by {artist_name}")
        return track_uris


    def get_spotify_song_uris(self, song_ids: List[dict]) -> List[str]:
        song_uris = []
        if len(song_ids) > 0:
            for song_id in song_ids:
                try:
                    track_uris = song_id["track_uris"]
                    try:
                        track_uri = track_uris[0]
                    except IndexError:
                        continue
                except KeyError:
                    continue
                song_uris.append(track_uri)
        return song_uris
        
    
    def create_empty_spotify_playlist(self, playlist_name: str) -> str:
        new_playlist = self.spotify.user_playlist_create(
            self.user_id, 
            playlist_name, 
            public = False
            )
        playlist_id = new_playlist["id"]
        return playlist_id


    def create_spotify_playlist(self, song_uris: List[str], playlist_name: str) -> None:
        if len(song_uris) > 0:
            playlist_id = self.create_empty_spotify_playlist(playlist_name)
            snapshot_id = self.spotify.user_playlist_add_tracks(
                self.user_id,
                playlist_id,
                song_uris
                )
            return snapshot_id
