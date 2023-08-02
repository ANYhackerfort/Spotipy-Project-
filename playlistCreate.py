import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime
from main import Environment
from main import UserInput

class NewPlayList(Environment):

    def __init__(self, playList, playListID):
        self.playList = playList
        self.playListID = playListID
        super().__init__() 
        environment = Environment()
        self.SpotifyObject = environment.spotifyObject
        self.username = environment.username
        self.sp = environment.sp


    def createPlaylist(self, playlist_name, playlist_description):
        newPlaylist = self.spotifyObject.user_playlist_create(self.username, playlist_name, public=True, collaborative=False, description=playlist_description)
        playlist_id = newPlaylist["id"]
        self.playListID = playlist_id
        print(playlist_id)
        return

    def addToPlaylist(self, songs):
        playlist_id = self.playListID
        print(playlist_id)
        self.spotifyObject.playlist_add_items(playlist_id, songs, position=0)

    def copyFromPlaylist(self, playlist_id):
        playList = self.spotifyObject.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
        songs = []

        for track in self.sp.playlist_tracks(playList["id"])["items"]:
            songs.append(track["track"]["uri"])
        
        self.addToPlaylist(songs)

    def organizeByYear(self, reverse=False): 
        dupleList = []
        playlist = []

        for track in self.sp.playlist_tracks(self.playListID)["items"]:
            track_uri = track["track"]["uri"]
            track_info = self.sp.track(track_uri)
            release_date = track_info["album"]["release_date"]
            yearTuple = (track_uri, release_date)
            dupleList.append(yearTuple)
        
        if reverse == False:
            dupleList = sorted(dupleList, key=lambda x: x[1])
        else:
            dupleList = sorted(dupleList, key=lambda x: x[1], reverse=True)

        for item in dupleList:
            playlist.append(item[0])

        self.spotifyObject.user_playlist_replace_tracks(self.username, self.playListID, playlist)

 
    # def organizeEmotions(self, reverse=False):
    #     for track in sp.playlist_tracks(self.playListID)["items"]:
    #         track_uri = track["track"]["uri"]
    #         track_info = sp.track(track_uri)
    #         release_date = track_info

if __name__ == "__main__":
    
    playlist = NewPlayList('playlistName', 'playlistID')
    userInput = UserInput('', '', '', '') 
    userInput.inputConsole() 
    playlist.createPlaylist(userInput.playlist_name, userInput.playlist_description)
    playlist.copyFromPlaylist(userInput.playlist_copy_from)
    playlist.organizeByYear(reverse=userInput.reverseYear)
