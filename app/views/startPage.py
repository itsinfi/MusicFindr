from flask import render_template, session
from app.services.playlistService import PlaylistService as p
from app.services import tagService as t
from app.services import userService
from app.services import voteService
        
class StartPage:
    @staticmethod
    def getStartPage():
        return render_template('content/start.html')
    
    @staticmethod
    def getDiscoverarea():
        
        shuffled_playlist = p.getShuffledPlaylist()
        playlists = {}
        for playlist in shuffled_playlist:
            playlistTagTuples = []
            for tagID in playlist.tags:
                tag = t.TagService.readTag(tagID)
                playlistTagTuples.append((playlist.id, tag))
            playlists[playlist.id] = sorted(playlistTagTuples, key = voteService.VoteService.getVoteNumberOnPlaylistTag, reverse = True)

        random_tags = t.TagService.getThreeRandomTags()
        
        return render_template('content/start.html', shuffled_playlist=shuffled_playlist, playlists=playlists, random_tags = random_tags, loggedin=userService.UserService.checkCurrentUserIsLoggedIn(), isStartPage=True)
 