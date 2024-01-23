from app.services import userService, playlistService
from flask import session, render_template, request, redirect

class SubmitPlaylistView():
    @staticmethod
    def loadPage() -> render_template:
        if userService.UserService.checkCurrentUserIsLoggedIn():

            if not (userService.UserService.checkCurrentUserIsLoggedIn()):
                return redirect("/")

            if request.method == 'POST':
                tags = playlistService.PlaylistService.tagsToTagList(request.form['tags'])
                playlistService.PlaylistService.createPlaylist(request.form['link'], request.form['title'], request.form['description'], tags, session['userId'])
                return redirect("/") 

            return render_template('content/submitPlaylist.html', loggedin=userService.UserService.checkCurrentUserIsLoggedIn(), username = userService.UserService.getSessionUsername)
    