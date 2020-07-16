import sys
import os.path
sys.path.insert(0, os.path.expanduser("~/.local/lib/python3.6/site-packages"))
import myauth
import json
import spotipy

scope = 'playlist-modify-private user-read-playback-state'
username = '1215249205'
exploreSONGS = '5qRm1EuT2P4hbKxu3eCI26'

def do_the_add(client, track_id):
    client.user_playlist_add_tracks(username, exploreSONGS, [track_id])

def get_current_track(client):
    data = client.current_playback()
    if data is not None:
        return data['item']['uri'].split(':')[2]
    else:
        exit

def get_client():
    return spotipy.Spotify(myauth.get_authoriziation(scope))

client = get_client()
do_the_add(client, get_current_track(client))
