import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from flask import Flask, redirect, url_for, session, request
from datetime import datetime

class Environment:
    
    def __init__(self):

        os.environ["SPOTIPY_CLIENT_ID"] = "ed5cbf589898495db2525f4a918ecdd5"
        os.environ["SPOTIPY_CLIENT_SECRET"] = "cf8d56c29a9c45b983e7933ebbee009b"
        os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8080/callback"

        #Client Login 
        client_credentials_manager = SpotifyClientCredentials(client_id='ed5cbf589898495db2525f4a918ecdd5', client_secret='cf8d56c29a9c45b983e7933ebbee009b')
        self.sp = sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

        #Authenticate With Account and specify permissions
        scope = 'playlist-modify-public playlist-modify-private'

        #Change to yours if you want to do testing on your computer
        self.username = username = session["spotify_username"]
        print(str(username))
        #Object and Token Creation
        token = SpotifyOAuth(scope=scope, username=username)
        self.spotifyObject = spotipy.Spotify(auth_manager = token)

class UserInput:
    

    def __init__(self, playlist_name, playlist_description, playlist_copy_from, reverseYear):

        self.playlist_name = playlist_name
        self.playlist_description = playlist_description
        self.playlist_copy_from = playlist_copy_from
        self.reverseYear = reverseYear

    def inputConsole(self):

        from backEndMethods import Tools

        self.playlist_name = input("Name of New Playlist: ")
        self.playlist_description = input("Description of New Playlist: ")
        link = input("Paste the link of the playlist you want to copy from: ")
        self.playlist_copy_from = Tools.cleanUpLink(link)
        self.reverseYear = Tools.stringCondition(input("New to Old (ENTER: True), Old to New (ENTER: False): ").lower())



