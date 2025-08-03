from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify


class AccountManager(object):
    def __init__(self, client_id = None, client_secret = None, redirect_uri = None,
                 scope: str = 'playlist-read-private user-read-email user-read-private user-follow-read user-library-read playlist-modify-public playlist-modify-private user-library-modify'
                 ) -> None:
        
        self._scope = scope
        self._sp = Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=self._scope))
        self._user = self._sp.current_user()
        
        if self._user is not None:
            self.user_id = self._user.get('id', 'Not found')
            self.username = self._user.get('display_name', 'Not found')
            self.country = self._user.get('country', 'Not found')
            self.email = self._user.get('email', 'Not found')
            self.user_type = self._user.get('type', 'Not found')
    
    
    def enumerate_playlists(self) -> (dict | None):
        playlists = self._sp.current_user_playlists()
        
        if playlists is None:
            return

        self.playlists = playlists['items']
        return self.playlists


    def enumerate_artists(self) -> (dict | None):
        artists = self._sp.current_user_followed_artists()
        
        if artists is None or (artists := artists.get('artists')) is None:
            return
        
        self.artists = artists.get('items', None)
        
        return self.artists