from flask import render_template


class View:
    @staticmethod
    def loadPage() -> render_template:
        pass

    @staticmethod
    def checkCurrentUserIsLoggedIn() -> bool:
        pass