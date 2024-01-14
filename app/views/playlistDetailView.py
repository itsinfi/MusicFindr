from app.views import view as v
from app.services import playlistService
from app.services import tagService
from flask import render_template

class PlaylistDetailView(v.View):
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
        

        return render_template('content/playlistDetail.html', pid = playlist.id, title = playlist.title, description = playlist.description, link = playlist.link, tags = tags)