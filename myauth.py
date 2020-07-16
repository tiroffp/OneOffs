import sys
import os.path
sys.path.insert(0, os.path.expanduser("~/.local/lib/python3.6/site-packages"))
import json
import webbrowser
import spotipy
from spotipy import oauth2
from bottle import Bottle, run, route, request, ServerAdapter

info_home = os.path.expanduser('~/.spotify/')
config_file = info_home + 'spotify_client_creds.json'
port = 8082
redirect_uri = 'http://localhost:' + str(port) + '/'
CACHE = info_home + '.spotipyoauthcache'

def get_authoriziation(scope):
    if not os.path.exists(config_file):
        print('No Credentials Found')
        print('Please add your client credentials to ~/.spotify/spotify_client_creds.json')
        exit()
    with open(config_file) as data_file:
        data = json.load(data_file)
    sp_oauth = oauth2.SpotifyOAuth( data['id'], data['secret'],redirect_uri,scope=scope,cache_path=CACHE )
    token_info = sp_oauth.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
        return access_token
    else:
        webbrowser.open(sp_oauth.get_authorize_url())
        app = Bottle()
        @app.route('/')
        def my_listener():
            access_token = ""
            url = request.url
            print(url)
            code = sp_oauth.parse_response_code(url)
            if code:
                print("Found Spotify auth code in Request URL! Trying to get valid access token...")
                token_info = sp_oauth.get_access_token(code)
                access_token = token_info['access_token']
            if access_token:
                print("Access token available!")
                sp = spotipy.Spotify(access_token)
                return access_token
                sys.stderr.close()
            else:
                return "an error occurred retrieving the access token -\_(o_o)_/-"
        app.run(host="localhost", port=port)
