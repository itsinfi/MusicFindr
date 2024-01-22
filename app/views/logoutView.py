from flask import redirect
from app.services import userService

@staticmethod
def logout():
    userService.UserService.logout()
    return redirect("/")