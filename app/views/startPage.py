from flask import render_template
from app.services.playlistService import PlaylistService as p
from app.services import tagService as t
        
class StartPage:
    @staticmethod
    def getStartPage():
        return render_template('content/start.html')
    
    @staticmethod
    def getDiscoverarea():
        
        shuffled_playlist = p.getShuffledPlaylist()
        tagTitles = {}
        for playlist in shuffled_playlist:
            playlistTagsTitles = []
            for tagID in playlist.tags:
                tag = t.TagService.readTag(tagID)
                playlistTagsTitles.append(tag.title)
            tagTitles[playlist.id] = playlistTagsTitles 

        random_tags = t.TagService.getThreeRandomTags()
        
        return render_template('content/start.html', shuffled_playlist=shuffled_playlist, playlists=tagTitles, random_tags = random_tags)
 