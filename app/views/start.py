from flask import render_template

class StartPage:
    @staticmethod
    def getStartPage():
        return render_template('start.html')