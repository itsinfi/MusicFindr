from datetime import datetime
from flask import Flask
from flask import url_for

from app import services as s
from app import models as m
from app import views as v
from app import components as c
# from flask_sqlalchemy import SQLAlchemy

def create_app():
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

    # ein bisschen CRUD mit Models durchspielen (nur zum Testen)
    try:
        s.user.UserService._createUser(1, '1_#passwordPasswordpassword', 'username1', datetime.now(), datetime.now())
        # print(s.user.UserService.readUser(1))
    except s.user.UserServiceError as e:
        print(e)
    # try:    
    #     s.user.UserService._createUser(1, 'password1', 'username1', datetime.now(), datetime.now())
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     s.user.UserService.createUser('passwort3', 'username1')
    # except s.user.UserServiceError as e:
    #     print(e)
    # print(s.user.UserService.allUsers)
    # try:
    #     s.user.UserService._createUser(2, 'password2', 'username2', datetime.now(), datetime.now())
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:    
    #     s.user.UserService._createUser(3, 'password3', 'username3', datetime.now(), datetime.now())
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     s.user.UserService.createUser('hehehehe', 'brotmann')
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     _uuuuserPW = s.user.UserService.readUser(4).password
    #     print(s.user.UserService.checkPassword('hehehehe', _uuuuserPW))
    #     print(s.user.UserService.checkPassword('qehehehe', _uuuuserPW))
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     s.user.UserService.readUser(2)
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     s.user.UserService.updateUser(2, 'password2', 'username2')
    # except s.user.UserServiceError:
    #     print(e)
    # print(s.user.UserService.allUsers)
    # try:
    #     s.user.UserService.deleteUser(4)
    # except s.user.UserServiceError:
    #     print(e)
    # try:
    #     s.user.UserService.deleteUser(3)
    # except s.user.UserServiceError:
    #     print(e)
    # try:
    #     s.user.UserService.deleteUser(1)
    # except s.user.UserServiceError:
    #     print(e)
    # try:
    #     s.user.UserService.readUser(1)
    # except s.user.UserServiceError as e:
    #     print(e)
    # print(s.user.UserService.allUsers)
    # try:
    #     _id = s.user.UserService.readUser(1).id
    #     s.playlist.PlaylistService._createPlaylist(1, "link1", "titel1", "beschreibung1", ["Tag1", "Tag2"], _id, datetime.now(), datetime.now())
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # except s.user.UserServiceError as e:
    #     print(e)
    try:
        _id = s.user.UserService.readUser(1).id
        s.playlist.PlaylistService._createPlaylist(1, "www.youtube.com/iqouweoiqwe", "titel1", "beschreibung1", [], _id, datetime.now(), datetime.now())
    except s.playlist.PlaylistServiceError as e:
        print(e)
    except s.user.UserServiceError as e:
        print(e)
    try:
        _id = s.user.UserService.readUser(1).id
        s.playlist.PlaylistService.createPlaylist("link1", "title1", "beschreibung1", [], _id)
    except s.user.UserServiceError as e:
        print(e)
    except s.playlist.PlaylistServiceError as e:
        print(e)
    # s.playlist.PlaylistService.playlistExists(1)
    # s.playlist.PlaylistService.playlistExists(2)
    # s.playlist.PlaylistService.linkExists("link1")
    # s.playlist.PlaylistService.linkExists("a")
    # try:
    #     s.playlist.PlaylistService.readPlaylist(1)
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # try:
    #     s.playlist.PlaylistService.readPlaylist(2)
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # try:
    #     s.playlist.PlaylistService.updatePlaylist(1, "1knil", "1letit", "1gnubierhcseb")
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # try:
    #     s.playlist.PlaylistService.deletePlaylist(1)
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # s.playlist.PlaylistService.playlistExists(1)
    # try:
    #     s.tag.TagService._createTag(3, "titel1", datetime.now())
    # except s.tag.TagServiceError as e:
    #     print(e)
    # try:
    #     s.tag.TagService._createTag(1,"titel1", datetime.now())
    # except s.tag.TagServiceError as e:
    #     print(e)
    # try:
    #     s.tag.TagService.createTag("titel1")
    # except s.tag.TagServiceError as e:
    #     print(e)
    # s.tag.TagService.tagExists(1)
    # s.tag.TagService.tagExists(2)
    # s.tag.TagService.titleExists("titel1")
    # s.tag.TagService.titleExists("a")
    # try:
    #     s.tag.TagService.readTag(1)
    # except s.tag.TagServiceError as e:
    #     print(e)
    # try:
    #     s.tag.TagService.readTag(2)
    # except s.tag.TagServiceError as e:
    #     print(e)
    # try:
    #     s.tag.TagService.updateTag(1,"1eltit")
    # except s.tag.TagServiceError as e:
    #     print(e)
    # try:
    #     s.tag.TagService.deleteTag(1)
    # except s.tag.TagServiceError as e:
    #     print(e)
    # s.tag.TagService.tagExists(1)
    # try:
    #     s.playlist.PlaylistService.updatePlaylist(1, "titel1", "beschreibung1", ["Tag1"])
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # print(s.tag.TagService.allTags)
    # try:
    #     s.vote.VoteService.createVote(1, 1, 1, 1)
    # except s.vote.VoteServiceError as e:
    #     print(e)
    # try:
    #     s.vote.VoteService.createVote(1, 1, 2, -1)
    # except s.vote.VoteServiceError as e:
    #     print(e)
    # try:
    #     s.vote.VoteService.createVote(1, 1, 1, 1)
    # except s.vote.VoteServiceError as e:
    #     print(e)
    # print(s.vote.VoteService.allVotes)
    # try:
    #     s.vote.VoteService.createVote(1, 1, 1, 0)
    # except s.vote.VoteServiceError as e:
    #     print(e)
    # print(s.vote.VoteService.allVotes)
    # try:
    #     s.vote.VoteService.updateVote(2, 0)
    # except s.vote.VoteServiceError as e:
    #     print(e)
    # print(s.vote.VoteService.allVotes)
    # print("DELETION TESTS--------------------------------------------------")
    # try:
    #     s.vote.VoteService.deleteVote(1)
    # except s.vote.VoteServiceError as e:
    #     print(e)
    # try:
    #     s.playlist.PlaylistService.deletePlaylist(1)
    # except s.playlist.PlaylistServiceError as e:
    #     print(e)
    # try:
    #     s.tag.TagService.deleteTag(2)
    # except s.tag.TagServiceError as e:
    #     print(e)
    # print(s.playlist.PlaylistService.allPlaylists)
    # try:
    #     s.user.UserService.deleteUser(1)
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     s.user.UserService._createUser(1, "passwort", "username", datetime.now(), datetime.now())
    # except s.user.UserServiceError as e:
    #     print(e)
    # try:
    #     s.user.UserService._createUser(1, "passwort", "username", datetime.now(), datetime.now())
    # except s.user.UserServiceError as e:
    #     print(e)
    # s.playlist.PlaylistService.updatePlaylist(1, "title1", "beschreibung1", ["titwweel1"])
    # print(s.playlist.PlaylistService.allPlaylists)
    # s.playlist.PlaylistService.updatePlaylist(1, "title1", "beschreibung1", ["titel1"])
    # print(s.playlist.PlaylistService.allPlaylists)
    # s.playlist.PlaylistService.addTag(1, "titwweel1")
    # print(s.playlist.PlaylistService.allPlaylists)
    # s.playlist.PlaylistService.addTag(1, "bruuuudder")
    # print(s.playlist.PlaylistService.allPlaylists)
    # s.playlist.PlaylistService.updatePlaylist(1, "title1", "beschreibung1", [])
    # print(s.playlist.PlaylistService.allPlaylists)
    
    # links = ["https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=ud_ZB4sRKhiBq81I", "https:usic.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=ud_ZB4sRKhiBq81I", "google.com", "http://google.com", "http://www.google.com"]
    # for link in links:
    #     print(s.playlist.PlaylistService.validateLink(link))
    
    # print(s.playlist.PlaylistService.validateTitle("Die Playlist von Hans, die es FETT in sich hat ✌✌✌"))
    
    # print(s.playlist.PlaylistService.validateLink("https://open.spotify.com/playlist/37i9dQZF1DXdLK5wjKyhVm?si=ff7c0e65767d47d9"))
    # print(s.playlist.PlaylistService.validateLink("https://www.youtube.com/playlist?list=PLNQeq1zOd4TcbTAkaW8Uer6m8OXMNKfJa"))
    # print(s.playlist.PlaylistService.validateLink("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=ud_ZB4sRKhiBq81I"))
    # print(s.playlist.PlaylistService.validateLink("https://soundcloud.com/infimusic/sets/dailykakas?si=59464911eebb48c49ab05d1df762b6d4&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing"))
    # print(s.playlist.PlaylistService.validateLink("https://on.soundcloud.com/R8JyR"))

    return app
