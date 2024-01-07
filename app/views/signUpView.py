from flask import render_template
from app.views import view as v

class SignUpView(v.View):
    @staticmethod
    def loadPage() -> render_template:
        # from app.services import userService
        from flask import render_template

        #TODO: add buttons, link buttons to functions, add return statement

        # try:
        return render_template('content/signUp.html')
        #TODO: add except statement, add custom error type
        # except 