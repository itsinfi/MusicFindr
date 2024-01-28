from app.services import playlistService
from app.services import tagService
from app.services import userService
from app.services import voteService
from flask import render_template, session

class PlaylistDetailView():
    @staticmethod
    def loadPage(pid: int) -> render_template:
        try:
            #Playlist lesen
            playlist = playlistService.PlaylistService.readPlaylist(int(pid))

            #Tags lesen
            tags = []
            for t in playlist.tags:
                try:
                    tag = tagService.TagService.readTag(t)
                except tagService.TagServiceError as e:
                    print(e)
                    continue
                tags.append((playlist.id, tag))
            
            #Votes lesen
            votes = {}
            if "username" in session:
                for playlistTagTuple in tags:
                    try:
                        vote = voteService.VoteService.findVote(session["userId"], playlist.id, playlistTagTuple[1].id)
                        votes[playlistTagTuple[1].id] = vote.voteValue
                    except voteService.VoteServiceError as e:
                        votes[playlistTagTuple[1].id] = 0
            else:
                for playlistTagTuple in tags:
                    votes[playlistTagTuple[1].id] = 0
            
            #CreatedBy auslesen
            try:
                user = userService.UserService.readUser(playlist.createdBy)
                createdBy = user.username
            except userService.UserServiceError as e:
                createdBy = "unknown"

            #Falls Playlist nicht gefunden
        except  playlistService.PlaylistServiceError as e:
            raise e

        return render_template('content/playlistDetail.html', pid = playlist.id, title = playlist.title, description = playlist.description, link = playlist.link, platform = playlist.platform, tags = sorted(tags, key = voteService.VoteService.getVoteNumberOnPlaylistTag, reverse = True), votes = votes, createdBy = createdBy, loggedin=userService.UserService.checkCurrentUserIsLoggedIn())