from app.services import userService, playlistService, tagService, voteService
from flask import session, render_template, request, redirect

class EditPlaylistView():
    @staticmethod
    def loadPage(playlist_id: int) -> render_template:
        if userService.UserService.checkCurrentUserIsLoggedIn():
            existing_playlist = playlistService.PlaylistService.readPlaylist(int (playlist_id))
            tags = []
            for t in existing_playlist.tags:
                try:
                    tag = tagService.TagService.readTag(t)
                except tagService.TagServiceError as e:
                    print(e)
                    continue
                tags.append((existing_playlist.id, tag))
            votes = {}
            if "username" in session:
                for playlistTagTuple in tags:
                    try:
                        vote = voteService.VoteService.findVote(session["userId"], existing_playlist.id, playlistTagTuple[1].id)
                        votes[playlistTagTuple[1].id] = vote.voteValue
                    except voteService.VoteServiceError as e:
                        votes[playlistTagTuple[1].id] = 0
            else:
                for playlistTagTuple in tags:
                    votes[playlistTagTuple[1].id] = 0

            if request.method == 'POST':
                if existing_playlist:
                    # Playlist bearbeiten
                    playlistService.PlaylistService.updatePlaylist(
                        int (playlist_id),
                        request.form['title'],
                        request.form['description'],
                        playlistService.PlaylistService.tagsToTagList(request.form['tags'])
                    )
                
                    return redirect('/profile')
                
            else:
                # Playlist nicht gefunden
                TagStrings=[]
                for tag in tags:
                    TagStrings.append(tag[1].title)
                return render_template('content/editPlaylist.html', loggedin=userService.UserService.checkCurrentUserIsLoggedIn(), username=userService.UserService.getSessionUsername(), tags = str(TagStrings).translate(str.maketrans('', '', f"\"[]'")), existing_playlist=existing_playlist)
        else:
            return redirect("/")