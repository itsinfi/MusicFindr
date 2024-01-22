from flask import render_template, request, redirect
from app.services import userService

class LoginView():
    @staticmethod
    def loadPage() -> render_template:
        # from app.services import userService
        from flask import render_template

        if request.method == 'POST':
            userService.UserService.login(request.form['password'], request.form['userName'])
            return redirect("/")

        return render_template('content/login.html', hidebutton=True)