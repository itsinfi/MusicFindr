from app.views import startPage
# from app.views import playlistDetail
from app.views import profileView
from app.views import signUpView
from app.views import loginView
from app.views import logoutView
from app.views import editProfileView
from app.views import searchresults
from app.views import playlistDetailView
from app.views import submitPlaylistView

from flask import Blueprint, app, render_template, request
from markupsafe import escape
# from app.components import errorDialog as e

blueprint = Blueprint('views', __name__)

#Routen für Views hier festlegen

@blueprint.route('/')
def start():
    return startPage.StartPage.getDiscoverarea()


@blueprint.route('/profile/<uid>')
def profile(uid: int):
    return profileView.ProfileView.loadPage(uid)

@blueprint.route('/signUp', methods = ['POST', 'GET'])
def signUp():
    #TODO:
    return signUpView.SignUpView.loadPage()

@blueprint.route('/login', methods = ['POST', 'GET'])
def login():
    #TODO:
    return loginView.LoginView.loadPage()

@blueprint.route('/logout')
def logout():
    return logoutView.logout()

@blueprint.route('/editProfile')
def editProfile():
    return editProfileView.EditProfileView.loadPage()

@blueprint.route('/playlist/<pid>', methods = ['POST', 'GET'])
def playlistDetail(pid: int):
    return playlistDetailView.PlaylistDetailView.loadPage(pid)

@blueprint.route('/submitPlaylist', methods = ['POST', 'GET'])
def submitPlaylist():
    return submitPlaylistView.SubmitPlaylistView.loadPage()

@blueprint.route('/search/<query>')
def search(query):
    return searchresults.SearchResults.loadPage(query)
