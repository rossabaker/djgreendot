import pyen
import spotipy
import spotipy.util as util
import sys

username = 'rossabaker'

token = util.prompt_for_user_token(username)
if not token:
    print "Can't get token for", username
    sys.exit(1)
sp = spotipy.Spotify(auth=token)

en = pyen.Pyen()

def find_playlist(name):
    playlists = sp.user_playlists(username)
    playlist = next((playlist for playlist in playlists['items'] if playlist['name'].lower() == name.lower()), None)
    if playlist:
        return playlist['id']

def create_playlist(name):
    if not find_playlist(name):
        sp.user_playlist_create(username, name, False)

def fill_playlist(name, genres):
    playlist_id = find_playlist(name)
    if playlist_id:
        en = pyen.Pyen()
        response = en.get('playlist/static', \
                type='genre-radio', \
                genre=genres, \
                results=100, \
                bucket=['tracks', 'id:spotify'], \
                limit='true',
                distribution='wandering')
        track_ids = [song['tracks'][0]['foreign_id'] for song in response['songs']]
        results = sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    else:
        print "Could not find playlist %s." % name

if (sys.argv[1] == '--find-playlist'):
    print find_playlist(sys.argv[2])
elif (sys.argv[1] == '--create-playlist'):
    create_playlist(sys.argv[2])
elif (sys.argv[1] == '--fill-playlist'):
    fill_playlist(sys.argv[2], sys.argv[3:])

