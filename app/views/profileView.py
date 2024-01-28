from flask import render_template, session
from app.services.playlistService import PlaylistService as p
from app.services import tagService as t
from app.services import userService
from app.services import voteService

class ProfileView():
    @staticmethod
    def loadPage():
        current_username = userService.UserService.getSessionUsername()
        current_user = userService.UserService.getUserViaUsername(current_username)

        # Alle Playlists des aktuellen Benutzers abrufen
        user_playlists = p.getUserPlaylists(current_user.id)

        

        playlists = {}
        for playlist in user_playlists:
            playlistTagTuples = []
            for tagID in playlist.tags:
                tag = t.TagService.readTag(tagID)
                playlistTagTuples.append((playlist.id, tag))
            playlists[playlist.id] = sorted(playlistTagTuples, key = voteService.VoteService.getVoteNumberOnPlaylistTag, reverse = True)

        
        return render_template('content/profile.html', user_playlists=user_playlists, playlists=playlists, current_user = current_user, current_username = current_username, loggedin=userService.UserService.checkCurrentUserIsLoggedIn(), isProfile = True)


