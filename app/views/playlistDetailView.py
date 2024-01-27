from app.services import playlistService
from app.services import tagService
from app.services import userService
from app.services import voteService
from flask import render_template, session

class PlaylistDetailView():
    @staticmethod
    def loadPage(pid: int) -> render_template:
        try:
            playlist = playlistService.PlaylistService.readPlaylist(int(pid))
            tags = {}
            for t in playlist.tags:
                try:
                    tag = tagService.TagService.readTag(t)
                except tagService.TagServiceError as e:
                    print(e)
                    continue
                tags[tag.id] = tag.title
            votes = {}
            if "username" in session:
                for tid in tags.keys():
                    try:
                        vote = voteService.VoteService.findVote(session["userId"], playlist.id, tid)
                        votes[tid] = vote.voteValue
                    except voteService.VoteServiceError as e:
                        votes[tid] = 0
            else:
                for tid in tags.keys():
                    votes[tid] = 0

        except  playlistService.PlaylistServiceError as e:
            raise e
        

        return render_template('content/playlistDetail.html', pid = playlist.id, title = playlist.title, description = playlist.description, link = playlist.link, tags = tags, votes = votes, loggedin=userService.UserService.checkCurrentUserIsLoggedIn())