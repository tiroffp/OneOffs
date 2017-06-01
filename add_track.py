import sys
import myauth
import spotipy

scope = 'playlist-modify-private'
username = '1215249205'
exploreSONGS = '5qRm1EuT2P4hbKxu3eCI26'
test ='22c2pt75xtnDddA5Zlm0yy'

def do_the_add(track_id):
    print(spotipy.Spotify(myauth.get_authoriziation(scope)).user_playlist_add_tracks(username, exploreSONGS, [track_id]))

do_the_add(sys.argv[1])