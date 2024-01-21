from flask import render_template, request
from app.views import view as v
from app.services import userService

class SignUpView(v.View):
    @staticmethod
    def loadPage() -> render_template:
        # from app.services import userService
        from flask import render_template

        if request.method == 'POST':
            userService.UserService.createUser(request.form['password'], request.form['userName'])


        #TODO: add return statement

        # try:
        return render_template('content/signUp.html')
        #TODO: add except statement, add custom error type
        # except 