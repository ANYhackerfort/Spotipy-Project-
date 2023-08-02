from flask import Flask, redirect, url_for, session, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from playlistCreate import NewPlayList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Spotify OAuth configuration
app.config['SPOTIPY_CLIENT_ID'] = 'ed5cbf589898495db2525f4a918ecdd5'
app.config['SPOTIPY_CLIENT_SECRET'] = 'cf8d56c29a9c45b983e7933ebbee009b'
app.config['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8080/callback'

# Initialize Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='ed5cbf589898495db2525f4a918ecdd5', redirect_uri='http://127.0.0.1:8080/callback', client_secret= 'cf8d56c29a9c45b983e7933ebbee009b', scope='user-library-read', cache_path='.spotipyoauthcache'))

@app.route('/')
def index():
    if 'spotify_username' in session:
        from main import UserInput

        # scope = 'playlist-modify-public playlist-modify-private'
        # token = SpotifyOAuth(scope=scope, username=session["spotify_username"])
        # spotifyObject = spotipy.Spotify(auth_manager = token)
        playlist = NewPlayList('playlistName', 'playlistID')
        userInput = UserInput('', '', '', '') 
        userInput.inputConsole()
        playlist.createPlaylist(userInput.playlist_name, userInput.playlist_description)
        playlist.copyFromPlaylist(userInput.playlist_copy_from)
        playlist.organizeByYear(reverse=userInput.reverseYear)

        return f'Hello, {session["spotify_username"]}!' 

    return 'Please <a href="/login">login with Spotify</a>'

@app.route('/login')
def login():
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp.auth_manager.get_access_token(code)
    session['spotify_token_info'] = token_info
    session['spotify_username'] = sp.me()['display_name']
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('spotify_token_info', None)
    session.pop('spotify_username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)