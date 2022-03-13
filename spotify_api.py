import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from os import getenv

CLIENT_ID = getenv('SPOTIPY_ID')
CLIENT_SECRET = getenv('SPOTIPY_CLIENT_SECRET')
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               scope=scope,
                                               redirect_uri='https://www.google.com/'))

playlists = sp.user_playlists('spotify')

print(sp.show_episodes(show_id='4uwiYvjNeIkafWJAx13CLc')['items'][0])
