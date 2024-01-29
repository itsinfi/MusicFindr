from datetime import datetime
from flask import Flask, jsonify, request, session
from flask import url_for

from app import services as s
from app import models as m
from app import views as v
from app import components as c
# from flask_sqlalchemy import SQLAlchemy

def create_app():
    # Dummy Daten laden (Anfoderung von Prototyp1)
    # s.dummyData.DummyDataService.loadDummyData()

    #App-Namen festlegen
    app = Flask("MusicFindr")

    # DB initialisieren
    s.sql.sqlService.init()

    # LIFE SAVER
    app.before_request(s.sql.sqlService.updateDB)

    # Config
    app.config['SECRET_KEY'] = 'your_secret_key'#TODO:

    app.register_blueprint(v.blueprint)

    #für ungültige routen
    @app.errorhandler(404)
    def pageNotFound(e):
        from flask import render_template
        return render_template('content/404.html'), 404
    
    #Bei jeglicher Exception wird ein Dialog angezeigt in der App:
    #Zwar kein guter Stil, aber eine einfache Lösung für unseren Prototypen Custom Error Messages zu definieren
    c.error.ErrorDialog.displayErrorMessage(app)

    @app.route('/vote', methods=['POST'])
    def vote():
        data = request.get_json()
        
        if "username" in session:
            tid = int(data.get("tid"))
            pid = int(data.get("pid"))
            uid = int(session["userId"])
            voteValue = int(data.get("voteValue"))
            
            vote = None

            try:
                vote = s.vote.VoteService.findVote(uid, pid, tid)
            except s.vote.VoteServiceError as e:
                print(e)
            try:
                if vote:
                    s.vote.VoteService.updateVote(vote.id, voteValue)
                else:
                    s.vote.VoteService.createVote(uid, pid, tid, voteValue)
                return jsonify({'status': 'success'})
            except s.vote.VoteServiceError as e:
                raise e
                
    @app.route('/addTagsToPlaylist', methods=['POST'])
    def addTagsToPlaylist():
        data = request.get_json()

        if "username" in session:
            pid = int(data.get("pid"))
            tagStrings = str(data.get("tagStrings"))

            additionalTags = s.playlist.PlaylistService.tagsToTagList(tagStrings)
            for tag in additionalTags:
                s.playlist.PlaylistService.addTag(pid, tag)
            return jsonify({'status': 'success'})
    
    @app.route('/deletePlaylist', methods=['POST'])
    def deletePlaylist():
        data = request.get_json()

        if "username" in session:
            pid = int(data.get("pid"))

            playlist = s.playlist.PlaylistService.readPlaylist(pid)
            
            if (int(session["userId"]) != playlist.createdBy):
                return
            
            s.playlist.PlaylistService.deletePlaylist(pid)
            return jsonify({'status': 'success'})
        
    @app.route('/updatePlaylist', methods=['POST'])
    def updatePlaylist():
        data = request.get_json()

        if "username" in session:
            pid = int(data.get("pid"))
            title = str(data.get("title"))
            description = str(data.get("description"))
            tags = str(data.get("tagStrings"))

            playlist = s.playlist.PlaylistService.readPlaylist(pid)

            if (int(session["userId"]) != playlist.createdBy):
                return

            s.playlist.PlaylistService.updatePlaylist(pid, title, description, s.playlist.PlaylistService.tagsToTagList(tags))
            return jsonify({'status': 'success'})
        
    #Alle Routen ausgeben (nur zum Testen)
    with app.test_request_context():
        print(url_for('views.start'))
        # print(url_for('views.profile', uid = 123))
        # print(url_for('views.playlist', pid = 123))
        print(url_for('views.search', query='Cyberpunk'))
        print(url_for('static', filename='style.css'))

    return app


