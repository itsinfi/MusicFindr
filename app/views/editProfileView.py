from flask import render_template
from app.services import userService

class EditProfileView():
    @staticmethod
    def loadPage() -> render_template:
        # from app.services import userService
        from flask import render_template

        #TODO: add return statement

        # try:
        return render_template('content/editProfile.html', loggedin=userService.UserService.checkCurrentUserIsLoggedIn())
        #TODO: add except statement, add custom error type
        # except 