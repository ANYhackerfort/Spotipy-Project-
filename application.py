from flask import Flask, redirect, url_for, session, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from playlistCreate import NewPlayList
from spotipy.cache_handler import CacheFileHandler


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Spotify OAuth configuration
app.config['SPOTIPY_CLIENT_ID'] = 'ed5cbf589898495db2525f4a918ecdd5'
app.config['SPOTIPY_CLIENT_SECRET'] = 'cf8d56c29a9c45b983e7933ebbee009b'
app.config['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8080/callback'

# Initialize Spotipy

class Environment():
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id='ed5cbf589898495db2525f4a918ecdd5', client_secret='cf8d56c29a9c45b983e7933ebbee009b')
        self.sp = sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        scope='playlist-modify-public playlist-modify-private user-read-private'
        cache_handler = CacheFileHandler(cache_path='.spotipyoauthcache')
        dp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='ed5cbf589898495db2525f4a918ecdd5', redirect_uri='http://127.0.0.1:8080/callback', client_secret= 'cf8d56c29a9c45b983e7933ebbee009b', scope=scope , cache_handler=cache_handler))
        user_info = dp.me()
        self.username = username = str(user_info['id'])
        code = request.args.get('code')
        token_info = dp.auth_manager.get_access_token(code, as_dict=False)
        self.spotifyObject = spotipy.Spotify(auth=token_info)

scope='playlist-modify-public playlist-modify-private user-read-private'
cache_handler = CacheFileHandler(cache_path='.spotipyoauthcache')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='ed5cbf589898495db2525f4a918ecdd5', redirect_uri='http://127.0.0.1:8080/callback', client_secret= 'cf8d56c29a9c45b983e7933ebbee009b', scope=scope , cache_handler=cache_handler))


def process_form_data(name, email, link, year, additionalChoices):

    from main import UserInput

    playlist = NewPlayList(name, email)
    userInput = UserInput(name, email, link, additionalChoices) 
    playlist.createPlaylist(userInput.playlist_name, userInput.playlist_description)
    playlist.copyFromPlaylist(userInput.playlist_copy_from)
    if year == "yes":
        #USE function attribute to track user's desires
        attributes = []
        playlist.organizeByYear(reverse=userInput.reverseYear)
        if request.form['yearOptions'] == "yes":
            order = "New to Old"
        else:
            order = "Old to New"
        attributes.append(f"Organized By Year: {order}")
        process_form_data.attributes = attributes

@app.route('/bobbylo', methods=['POST'])
def siyes():
    if request.method == 'POST':
        # Get form data from the request object
        name = str(request.form['name'])
        email = str(request.form['description'])
        link = str(request.form['link'])
        year = str(request.form['year'])
        if year == "yes":
            additionalChoices = str(request.form['yearOptions'])
        additionalChoices = "null" 
        # Call the method to process the form data
        process_form_data(name, email, link, year, additionalChoices)
        status = "Your Playlist is Ready!"
        attributes = process_form_data.attributes
        text = "Features you chose:"
        user_info = sp.me()
        greeting_message = f"Hello, {user_info['display_name']}. You are now connected with Spotify!!"
        return render_template("index.html", status=status, attributes=attributes, text=text, greeting_message=greeting_message)

@app.route('/')
def index():
    if 'spotify_token_info' in session:
        user_info = sp.me()
        greeting_message = f"Hello, {user_info['display_name']}. You are now connected with Spotify!	☆	☆	☆"
        return render_template("index.html", greeting_message = greeting_message)
    status = "Not Logged In"
    return render_template("placeholder.html", status = status)

@app.route('/login')
def login():
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp.auth_manager.get_access_token(code, as_dict=False)
    session['spotify_token_info'] = token_info
    try:
        user_info = sp.me()
        session['spotify_username'] = user_info['id']
    except spotipy.SpotifyException:
        session['spotify_username'] = None
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('spotify_token_info', None)
    session.pop('spotify_username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    
# @app.route('/button_clicked', methods=['POST'])
# def button_clicked():
#     from main import UserInput

#     playlist = NewPlayList('playlistName', 'playlistID')
#     userInput = UserInput('', '', '', '') 
#     userInput.inputConsole()
#     playlist.createPlaylist(userInput.playlist_name, userInput.playlist_description)
#     playlist.copyFromPlaylist(userInput.playlist_copy_from)
#     playlist.organizeByYear(reverse=userInput.reverseYear)
#     return "Check your newest created playlist! It's there!"