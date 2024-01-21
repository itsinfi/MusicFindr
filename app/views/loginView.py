from flask import render_template, request
from app.views import view as v
from app.services import userService

class LoginView(v.View):
    @staticmethod
    def loadPage() -> render_template:
        # from app.services import userService
        from flask import render_template

        if request.method == 'POST':
            userService.UserService.login(request.form['password'], request.form['userName'])

        return render_template('content/login.html')