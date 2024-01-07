from app.views import startPage
# from app.views import playlistDetail
from app.views import profileView
from app.views import signUpView
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

# @blueprint.route('/playlist/<pid>')
# def playlist(pid):
#     return playlistDetail.PlaylistDetailView.loadPage(pid)

@blueprint.route('/search/<query>')
def search(query):
    return f'Zeige Resultate für Suche nach {escape(query)}'