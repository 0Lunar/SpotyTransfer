from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import os


class AccountManager(object):
    def __init__(self, client_id = None, client_secret = None, redirect_uri = None,
                 scope: list | None = None
                 ) -> None:
    
        if scope is None:
            scope = ['playlist-read-private', 'user-read-email', 'user-read-private', 'user-follow-read', 'user-library-read', 'playlist-modify-public', 'playlist-modify-private', 'user-library-modify']
    
        client_id = client_id or os.environ.get("SPOTIPY_CLIENT_ID", None)
        client_secret = client_secret or os.environ.get("SPOTIPY_CLIENT_SECRET", None)
        redirect_uri = redirect_uri or os.environ.get("SPOTIPY_REDIRECT_URI", None)
    
        if client_id is None:
            raise EnvironmentError("Missing SPOTIPY_CLIENT_ID")
    
        if client_secret is None:
            raise EnvironmentError("Missing SPOTIPY_CLIENT_SECRET")
    
        if redirect_uri is None:
            raise EnvironmentError("Missing SPOTIPY_REDIRECT_URI")
        
        self._scope = ' '.join(scope)
        self._sp = Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=self._scope))
        self._user = self._sp.current_user()
        
        if self._user is not None:
            self.user_id = self._user.get('id', 'Not found')
            self.username = self._user.get('display_name', 'Not found')
            self.country = self._user.get('country', 'Not found')
            self.email = self._user.get('email', 'Not found')
            self.user_type = self._user.get('type', 'Not found')
    
    
    def get_playlists(self) -> (list[dict] | None):
        try:
            playlists = self._sp.current_user_playlists()
    
            if playlists is None:
                return None
        
            self.playlists = playlists['items']
            return self.playlists
        except:
            return None


    def get_playlist_tracks(self, playlist_id: str, max_tracks: int = 100, offset: int = 0) -> (dict | None):
        try:
            tracks = self._sp.playlist_tracks(playlist_id, limit=max_tracks, offset=offset)
        
            if tracks is None:
                return None
        
            self.tracks = tracks
            return tracks
        except:
            return None
    
    
    def make_playlist(self, name: str, public: bool = True, collaborative: bool = False, description: str = "") -> (dict | None):
        try:
            result = self._sp.user_playlist_create(self.user_id, name, public, collaborative, description)
        
            if result is None:
                return None
        
            return {
                "url": result['external_urls']['spotify'],
                "id": result['id'],
            }
        
        except:
            return None
    
    
    def add_playlist_tracks(self, playlist_id: str, tracks_uri: list, position: int | None = None) -> (bool | None):
        try:
            self._sp.playlist_add_items(playlist_id, tracks_uri, position=None)
            return True
        except:
            return None
    
    
    def clone_playlist(self, playlist_id: str, new_name: str, max_tracks: int = 100, offset: int = 0) -> (dict | None):
        tracks = []
        
        while max_tracks > 100:
            t = self.get_playlist_tracks(playlist_id, 100, offset)
            
            if t is None:
                break
        
            tracks += t['items']
            max_tracks -= 100
            offset += 100
        
        if max_tracks > 0:
            t = self.get_playlist_tracks(playlist_id, max_tracks, offset)
            
            if t is not None:
                tracks += t['items']
        
        if tracks is None:
            return None
        
        new_playlist = self.make_playlist(new_name)
        
        if new_playlist is None:
            return None
                
        track_uris = [track['track']['uri'] for track in tracks]
        track_uris = [track_uris[i:i+100] for i in range(0, len(track_uris), 100)]
        
        for t in range(len(track_uris)):
            success = self.add_playlist_tracks(new_playlist['id'], track_uris[t], t*100)

            if not success:
                return None
        
        return new_playlist