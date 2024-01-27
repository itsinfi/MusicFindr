from flask import render_template
from app.services import userService, playlistService as p, voteService, tagService as t
from datetime import datetime

class SearchResults():
    @staticmethod
    def loadPage(query: str) -> render_template:
        
        try:
            playlists = {}
            if not query:  # Überprüfen, ob der Suchquery leer ist
                raise p.PlaylistQueryServiceError
            else:
                result = p.PlaylistService.searchPlaylist(query)
                if not result:
                    raise p.PlaylistSearchServiceError(query)
                for playlist in result:
                    playlistTagTuples = []
                    for tagID in playlist.tags:
                        try:
                            tag = t.TagService.readTag(tagID)
                        except t.TagServiceError as e:
                            print(e)
                            continue
                        playlistTagTuples.append((playlist.id, tag))
                    playlists[playlist.id] = sorted(playlistTagTuples, key = voteService.VoteService.getVoteNumberOnPlaylistTag, reverse = True)
            return render_template('content/searchResults.html', query=query, result=result, playlists=playlists, loggedin=userService.UserService.checkCurrentUserIsLoggedIn())
        except p.PlaylistSearchServiceError as e:
            raise e

   
