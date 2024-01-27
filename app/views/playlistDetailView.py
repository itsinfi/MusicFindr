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
            tags = []
            for t in playlist.tags:
                try:
                    tag = tagService.TagService.readTag(t)
                except tagService.TagServiceError as e:
                    print(e)
                    continue
                tags.append((playlist.id, tag))
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

        except  playlistService.PlaylistServiceError as e:
            raise e
        
        embeddedLink = False
        if (playlist.platform == "spotify"):
            playlistID = playlist.link.split('/')[-1].split('?')[0]
            embeddedLink = f"https://open.spotify.com/embed/playlist/{playlistID}"

        return render_template('content/playlistDetail.html', pid = playlist.id, title = playlist.title, description = playlist.description, link = playlist.link, platform = playlist.platform, embeddedLink = embeddedLink, tags = sorted(tags, key = voteService.VoteService.getVoteNumberOnPlaylistTag, reverse = True), votes = votes, loggedin=userService.UserService.checkCurrentUserIsLoggedIn())