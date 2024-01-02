from datetime import datetime
from flask import Flask
from flask import url_for

from app import services as s
from app import models as m
from app import views as v
# from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask("MusicFindr")

    # Config
    app.config['SECRET_KEY'] = 'your_secret_key'#TODO:
    # app.config['SQLALCHEMY_DATABASE_URI'] = '' #TODO:
    # db = SQLAlchemy(app)

    app.register_blueprint(v.blueprint)
    
    #Alle Routen ausgeben (nur zum Testen)
    with app.test_request_context():
        print(url_for('views.start'))
        print(url_for('views.profile', uid = 123))
        print(url_for('views.playlist', pid = 123))
        print(url_for('views.search', query='Cyberpunk'))
        print(url_for('static', filename='style.css'))

    #ein bisschen CRUD mit Models durchspielen (nur zum Testen)
    s.user.UserService._createUser(1, 'password1', 'username1', datetime.now(), datetime.now())
    # s.user.UserService._createUser(1, 'password1', 'username1', datetime.now(), datetime.now())
    # s.user.UserService.createUser('passwort3', 'username1')
    # print(s.user.UserService.allUsers)
    # s.user.UserService._createUser(2, 'password2', 'username2', datetime.now(), datetime.now())
    # s.user.UserService._createUser(3, 'password3', 'username3', datetime.now(), datetime.now())
    # s.user.UserService.createUser('hehehehe', 'brotmann')
    # print(s.user.UserService.checkPassword('hehehehe', s.user.UserService.readUser(4).password))
    # print(s.user.UserService.checkPassword('qehehehe', s.user.UserService.readUser(4).password))
    # s.user.UserService.readUser(2)
    # s.user.UserService.updateUser(2, 'password2', 'username2')
    # print(s.user.UserService.allUsers)
    # s.user.UserService.deleteUser(4)
    # s.user.UserService.deleteUser(3)
    # s.user.UserService.deleteUser(1)
    # s.user.UserService.readUser(1)
    # print(s.user.UserService.allUsers)
    s.playlist.PlaylistService._createPlaylist(1, "link1", "titel1", "beschreibung1", ["Tag1", "Tag2"], s.user.UserService.readUser(1).id, datetime.now(), datetime.now())
    # s.playlist.PlaylistService._createPlaylist(1, "link1", "titel1", "beschreibung1", [], s.user.UserService.readUser(1).id, datetime.now(), datetime.now())
    # s.playlist.PlaylistService.createPlaylist("link1", "title1", "beschreibung1", [], s.user.UserService.readUser(1).id)
    # s.playlist.PlaylistService.playlistExists(1)
    # s.playlist.PlaylistService.playlistExists(2)
    # s.playlist.PlaylistService.linkExists("link1")
    # s.playlist.PlaylistService.linkExists("a")
    # s.playlist.PlaylistService.readPlaylist(1)
    # s.playlist.PlaylistService.readPlaylist(2)
    # s.playlist.PlaylistService.updatePlaylist(1, "1knil", "1letit", "1gnubierhcseb")
    # s.playlist.PlaylistService.deletePlaylist(1)
    # s.playlist.PlaylistService.playlistExists(1)
    s.tag.TagService._createTag(3, "titel1", datetime.now())
    # s.tag.TagService._createTag(1,"titel1", datetime.now())
    # s.tag.TagService.createTag("titel1")
    # s.tag.TagService.tagExists(1)
    # s.tag.TagService.tagExists(2)
    # s.tag.TagService.titleExists("titel1")
    # s.tag.TagService.titleExists("a")
    # s.tag.TagService.readTag(1)
    # s.tag.TagService.readTag(2)
    # s.tag.TagService.updateTag(1,"1eltit")
    # s.tag.TagService.deleteTag(1)
    # s.tag.TagService.tagExists(1)
    # s.playlist.PlaylistService.updatePlaylist(1, "link1", "titel1", "beschreibung1", ["Tag1"])
    print(s.tag.TagService.allTags)
    s.vote.VoteService.createVote(1, 1, 1, 1)
    s.vote.VoteService.createVote(1, 1, 2, -1)
    s.vote.VoteService.createVote(1, 1, 1, 1)
    print(s.vote.VoteService.allVotes)
    # s.vote.VoteService.createVote(1, 1, 1, 0)
    print(s.vote.VoteService.allVotes)
    # s.vote.VoteService.updateVote(2, 0)
    print(s.vote.VoteService.allVotes)
    print("DELETION TESTS--------------------------------------------------")
    # s.vote.VoteService.deleteVote(1)
    # s.playlist.PlaylistService.deletePlaylist(1)
    # s.tag.TagService.deleteTag(2)
    # print(s.playlist.PlaylistService.allPlaylists)
    s.user.UserService.deleteUser(1)

    return app
