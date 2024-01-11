
from app.views import view as v
from flask import render_template

class ProfileView(v.View):
    @staticmethod
    def loadPage(uid: int) -> render_template:
        from app.services import userService
        from datetime import datetime

        # TODO:remove later
        try:
            userService.UserService._createUser(2, "blaB223#981273_", "nutzernameeeee", datetime.now(), datetime.now())
        except userService.UserServiceError as e:
            print(e)

        try:
            result = userService.UserService.readUser(int(uid))
            return render_template('content/profile.html', username = result.username)
        except userService.UserServiceError as e:
            raise e


