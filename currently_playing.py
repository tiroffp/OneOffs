#!usr/bin/python3

import sys
import os.path
sys.path.insert(0, os.path.expanduser("~/.local/lib/python3.6/site-packages"))
import myauth
import json
import spotipy

scope = 'user-read-playback-state'
username = '1215249205'

def get_client():
    return spotipy.Spotify(myauth.get_authoriziation(scope))

def currently_playing(client):
    data = client.current_playback()
    if data is not None:
        test = f'{data}'
        print(f'♫ {data["item"]["name"]} - {data["item"]["artists"][0]["name"]}', end='')
    else:
        exit

currently_playing(get_client())


