from app.views import startPage
from app.views import playlistDetail
from app.views import profile as _profile
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
    return _profile.ProfileView.loadPage(uid)

@blueprint.route('/playlist/<pid>')
def playlist(pid):
    return playlistDetail.PlaylistDetailView.loadPage(pid)

@blueprint.route('/search/<query>')
def search(query):
    return f'Zeige Resultate für Suche nach {escape(query)}'