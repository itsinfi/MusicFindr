from flask import Flask
from flask import url_for

def create_app():
    app = Flask("MusicFindr")

    # Config
    app.config['SECRET_KEY'] = 'your_secret_key'#TODO:

    from app.views import blueprint
    app.register_blueprint(blueprint)
    
    #Alle Routen ausgeben (nur zum Testen)
    with app.test_request_context():
        print(url_for('views.start'))
        print(url_for('views.profile', uid = 123))
        print(url_for('views.playlist', pid = 123))
        print(url_for('views.search', query='Cyberpunk'))
        print(url_for('static', filename='style.css'))

    return app
