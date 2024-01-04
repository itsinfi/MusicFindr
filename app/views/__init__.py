from app.views import startPage
from flask import Blueprint
from markupsafe import escape
# from app.components import errorDialog as e

blueprint = Blueprint('views', __name__)

#Routen für Views hier festlegen

@blueprint.route('/')
def start():
    return startPage.StartPage.getStartPage()

#erstmal nur beispielhaft
@blueprint.route('/profile/<uid>')
# @e.dialogDecorator
def profile(uid: int):
    from app.services import userService
    from flask import render_template
    from datetime import datetime
    
    try:
        userService.UserService._createUser(2, "bla", "nutzernameeeee", datetime.now(), datetime.now())
    except userService.UserServiceError as e:
        print(e)

    try:
        result = userService.UserService.readUser(int(uid))
        print(f"REEEESULT={result}")
        return render_template('content/profile.html', username = result.username)
    except userService.UserServiceError as e:
        print(e)
        # return render_template('content/profile.html', username = "not found", dialog = True, error_message = e)
        raise e
    # return f'Benutzer mit ID: {escape(uid)}'

@blueprint.route('/playlist/<pid>')
def playlist(pid):
    return f'Playlist mit ID {escape(pid)}'

@blueprint.route('/search/<query>')
def search(query):
    return f'Zeige Resultate für Suche nach {escape(query)}'