from flask import render_template
from app.views import view as v

class SearchResults(v.View):
    @staticmethod
    def loadPage(query: str) -> render_template:
        from app.services import userService as u, playlistService as p, tagService as t
        from datetime import datetime

        # TODO:remove later
        try:
            u.UserService.createUser("Zufall1!" , "beispiel1")
            t.TagService.createTag("Metal")
            t.TagService.createTag("cool")
            user = u.UserService.readUser(1)
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=bs0b-FS3o9BsNfls", "Coole Playlist", "OK", ["Metal"], 1)
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=bs0b-FS3o9BsNfls", "Coole Playlist", "OK", ["cool"], 1)
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=bs0b-FS3o9BsNfls", "Coole Playlist", "OK", ["Metal", "cool"], 1)
        except u.UserServiceError as e:
            raise e
        except p.PlaylistServiceError as e:
            raise e
        except t.TagServiceError as e:
            raise e

        try:
            result = p.PlaylistService.searchPlaylist("Metal")
            return render_template('content/searchResults.html', query = query, result = result)
        except u.UserServiceError as e:
            raise e