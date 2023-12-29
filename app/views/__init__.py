from app.views.start import StartPage
from flask import Blueprint
from markupsafe import escape

blueprint = Blueprint('views', __name__)

#Routen für Views hier festlegen

@blueprint.route('/')
def start():
    return StartPage.getStartPage()

@blueprint.route('/profile/<uid>')
def profile(uid):
    return f'Benutzer mit ID: {escape(uid)}'

@blueprint.route('/playlist/<pid>')
def playlist(pid):
    return f'Playlist mit ID {escape(pid)}'

@blueprint.route('/search/<query>')
def search(query):
    return f'Zeige Resultate für Suche nach {escape(query)}'