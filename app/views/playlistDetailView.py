from app.services import playlistService
from app.services import tagService
from app.services import userService
from flask import render_template, request

class PlaylistDetailView():
    @staticmethod
    def loadPage(pid: int) -> render_template:
        try:
            playlist = playlistService.PlaylistService.readPlaylist(int(pid))
            tags = []
            for t in playlist.tags:
                try:
                    tag = tagService.TagService.readTag(t)
                except tagService.TagServiceError as e:
                    print(e)
                    continue
                tags.append(tag.title)
        except  playlistService.PlaylistServiceError as e:
            raise e
        

        return render_template('content/playlistDetail.html', pid = playlist.id, title = playlist.title, description = playlist.description, link = playlist.link, tags = tags, loggedin=userService.UserService.checkCurrentUserIsLoggedIn())