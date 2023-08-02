import os

class Tools:

    def cleanUpLink(link):
        question_mark_index = link.find("?")
        link.split('https://open.spotify.com/playlist')
        cleaned = link[:question_mark_index] 
        return str(cleaned) 

    def stringCondition(input):
        if input == 'true':
            return True
        else:
            return False 