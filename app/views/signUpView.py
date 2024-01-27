from flask import render_template, request, redirect
from app.services import userService

class SignUpView():
    @staticmethod
    def loadPage() -> render_template:
        # from app.services import userService
        from flask import render_template

        if (userService.UserService.checkCurrentUserIsLoggedIn()):
            return redirect("/")

        if request.method == 'POST':
            try:
                usernameError = ""
                userService.UserService.validateUsername(request.form['userName'])
            except userService.UserServiceError as e:
                usernameError = e

            try:
                passwordError = ""
                userService.UserService.validatePassword(request.form['password'])
            except userService.UserServiceError as e:
                passwordError = e

            if usernameError or passwordError:
                return render_template('content/signUp.html', hidebutton=True, usernameError = usernameError, passwordError = passwordError)
            else:
                userService.UserService.createUser(request.form['password'], request.form['userName'])
                return redirect("/login")
            
        
        return render_template('content/signUp.html', hidebutton=True, usernameError = False, passwordError = False)