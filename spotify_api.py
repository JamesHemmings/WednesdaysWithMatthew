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

podcast = sp.show_episodes(show_id='4uwiYvjNeIkafWJAx13CLc')
episodes = podcast['items']
while podcast['next']:
    episodes.extend(sp.next(podcast)['items'])
    podcast = sp.next(podcast)


def search_episodes(search_term, episode_list):
    results = []
    for episode in episode_list:
        for key in episode:
            if search_term.lower() in str(episode[key]).lower():
                results.append(episode)
                break
    return results
