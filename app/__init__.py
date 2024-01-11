from datetime import datetime
from flask import Flask
from flask import url_for

from app import services as s
from app import models as m
from app import views as v
from app import components as c
# from flask_sqlalchemy import SQLAlchemy

def create_app():
    #Dummy Daten laden (Anfoderung von Prototyp1)
    s.dummyData.DummyDataService.loadDummyData()

    #App-Namen festlegen
    app = Flask("MusicFindr")

    # Config
    app.config['SECRET_KEY'] = 'your_secret_key'#TODO:
    # app.config['SQLALCHEMY_DATABASE_URI'] = '' #TODO:
    # db = SQLAlchemy(app)

    app.register_blueprint(v.blueprint)

    #für ungültige routen
    @app.errorhandler(404)
    def pageNotFound(e):
        from flask import render_template
        return render_template('content/404.html'), 404
    
    #Bei jeglicher Exception wird ein Dialog angezeigt in der App:
    #Zwar kein guter Stil, aber eine einfache Lösung für unseren Prototypen Custom Error Messages zu definieren
    c.error.ErrorDialog.displayErrorMessage(app)
    
    #Alle Routen ausgeben (nur zum Testen)
    with app.test_request_context():
        print(url_for('views.start'))
        # print(url_for('views.profile', uid = 123))
        # print(url_for('views.playlist', pid = 123))
        print(url_for('views.search', query='Cyberpunk'))
        print(url_for('static', filename='style.css'))

    return app
