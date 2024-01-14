from flask import render_template
from app.views import view as v

class SearchResults(v.View):
    @staticmethod
    def loadPage(query: str) -> render_template:
        from app.services import userService as u, playlistService as p, tagService as t
        from datetime import datetime
        
        try:
            tagTitles = {}
            if not query:  # Überprüfen, ob der Suchquery leer ist
                raise p.PlaylistQueryServiceError
            else:
                result = p.PlaylistService.searchPlaylist(query)
                if not result:
                    raise p.PlaylistSearchServiceError(query)
                for playlist in result:
                    playlistTagsTitles = []
                    for tagID in playlist.tags:
                        try:
                            tag = t.TagService.readTag(tagID)
                        except t.TagServiceError as e:
                            print(e)
                            continue
                        playlistTagsTitles.append(tag.title)
                    tagTitles[playlist.id] = playlistTagsTitles
            return render_template('content/searchResults.html', query=query, result=result, playlists=tagTitles)
        except p.PlaylistSearchServiceError as e:
            raise e

   
