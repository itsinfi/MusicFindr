from app.views import view as v
from app.services import playlistService
from flask import render_template

class PlaylistDetailView(v.View):
    @staticmethod
    def loadPage(pid: int) -> render_template:
        playlist = playlistService.PlaylistService.readPlaylist(pid)
        tags = ""
        for t in playlist.tags:
            tags = tags+t
        

        return render_template('content/playlistDetail.html', pid = playlist.pid, title = playlist.title, description = playlist.description, link = playlist.link, tags = tags)