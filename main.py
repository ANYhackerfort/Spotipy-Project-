import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from flask import Flask, redirect, url_for, session, request
from datetime import datetime


class UserInput:
    

    def __init__(self, playlist_name, playlist_description, playlist_copy_from, reverseYear):

        from backEndMethods import Tools

        self.playlist_name = playlist_name
        self.playlist_description = playlist_description
        self.playlist_copy_from = playlist_copy_from
        self.reverseYear = Tools.stringCondition(reverseYear)

    # def inputConsole(self):

    #     from backEndMethods import Tools

    #     self.playlist_name = input("Name of New Playlist: ")
    #     self.playlist_description = input("Description of New Playlist: ")
    #     link = input("Paste the link of the playlist you want to copy from: ")
    #     self.playlist_copy_from = Tools.cleanUpLink(link)
    #     self.reverseYear = Tools.stringCondition(input("New to Old (ENTER: True), Old to New (ENTER: False): ").lower())

