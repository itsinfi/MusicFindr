from app.views import startPage
# from app.views import playlistDetail
from app.views import profileView
from app.views import signUpView
from app.views import editProfileView
from app.services import signUpService
from app.views import searchresults
from app.views import playlistDetailView

from flask import Blueprint
from markupsafe import escape
# from app.components import errorDialog as e

blueprint = Blueprint('views', __name__)

#Routen für Views hier festlegen

@blueprint.route('/')
def start():
    return startPage.StartPage.getStartPage()

@blueprint.route('/profile/<uid>')
def profile(uid: int):
    return profileView.ProfileView.loadPage(uid)

@blueprint.route('/signUp')
def signUp():
    #TODO:
    return signUpView.SignUpView.loadPage()

@blueprint.route('/submit')
def submit():
    return signUpService.SignUpService.submit()

@blueprint.route('/editProfile')
def editProfile():
    return editProfileView.EditProfileView.loadPage()

@blueprint.route('/playlist/<pid>')
def playlistDetail(pid: int):
    return playlistDetailView.PlaylistDetailView.loadPage(pid)

@blueprint.route('/search/<query>')
def search(query):
    return searchresults.SearchResults.loadPage(query)

