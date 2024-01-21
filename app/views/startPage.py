from flask import render_template

class StartPage:
    @staticmethod
    def getStartPage():
        return render_template('content/start.html')
    
    @staticmethod
    def getDiscoverarea():
        from app.services.playlistService import PlaylistService as p
        
        shuffled_playlist = p.getShuffledPlaylist()
        return render_template('content/start.html', shuffled_playlist=shuffled_playlist)