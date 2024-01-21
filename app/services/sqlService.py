from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
import json

class sqlServiceError(Exception):
    """
    Custom Error Klasse für Methoden des SQLService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class sqlService:
    
    engine = None
    session = None
    base = None

    trashBin = []

    @staticmethod
    def init():
        jsonfile = "dbConnection.json"
        with open(jsonfile, 'r') as file:
            dbCreds = json.loads(file.read())
        #mysql+pymysql://username:password@host:port/database_name
        dbUri = f"mysql+pymysql://{dbCreds['data']['user']}:{dbCreds['data']['password']}@{dbCreds['data']['host']}:{dbCreds['data']['port']}/{dbCreds['data']['dbName']}"
        
        sqlService.engine = create_engine(dbUri)
        sqlService.base = declarative_base()
        sqlService.base.metadata.create_all(sqlService.engine)
        sqlService.session = sessionmaker(bind=sqlService.engine)
        sqlService.readDB()

    @staticmethod
    def create(tableName:str, keys:str, values:str):
        with sqlService.engine.connect() as connection:
            query = text(f"INSERT INTO {tableName} ({keys}) VALUES ({values});")
            connection.execute(query)
            connection.commit()

    @staticmethod
    def read(tableName: str):
        query = text(f"SELECT * FROM {tableName};")
        with sqlService.engine.connect() as connection:
            result = connection.execute(query)
            data_variable = result.fetchall()
            table = {}
            for row in data_variable:
                rowMapping = row._mapping
                id = rowMapping["id"]
                table[id] = rowMapping
            return table
    
    @staticmethod
    def update(tableName:str, id:int, key:str, value:str):
        with sqlService.engine.connect() as connection:
            query = text(f"UPDATE {tableName} SET {key} = {value} WHERE id = {id};")
            connection.execute(query)
            connection.commit()
    
    @staticmethod
    def delete(model, primary_key):
        with sqlService.session() as session:
            instance = session.query(model).get(primary_key)
            if instance:
                session.delete(instance)
                session.commit()

    @staticmethod
    def trash(item):
        sqlService.trashBin.append(item)
  
    @staticmethod
    def updateDB():
        sqlService.updateUsers()
        sqlService.updatePlaylists()
        sqlService.updateTags()
        sqlService.updateVotes()
        sqlService.updatePlaylistTags()
        sqlService.deleteTrashBinItems()

    @staticmethod
    def updateUsers():
        from app.services import userService as u
        appUsers = u.UserService.allUsers
        try:
            table = "User"
            dbUsers = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        for appUser in appUsers:
            if appUser.id in dbUsers:
                dbUser = dbUsers[appUser.id]
                if (appUser.username != dbUser["username"]):
                    sqlService.update(table, appUser.id, "username", f"\"{appUser.username}\"")
                if (appUser.password != dbUser["password"]):
                    sqlService.update(table, appUser.id, "password", f"\"{appUser.password}\"")
                if(appUser.createdAt != dbUser["createdAt"]):
                    sqlService.update(table, appUser.id, "createdAt", f"{appUser.createdAt}")
                if(appUser.createdAt != dbUser["updatedAt"]):
                    sqlService.update(table, appUser.id, "updatedAt", f"{appUser.updatedAt}")
            else:
                sqlService.create(table, "id, username, password, createdAt, updatedAt", f"{appUser.id}, \"{appUser.username}\", \"{appUser.password}\", {appUser.createdAt}, {appUser.updatedAt}")
        return

    @staticmethod
    def updatePlaylists():
        from app.services import playlistService as p
        appPlaylists = p.PlaylistService.allPlaylists
        try:
            table = "Playlist"
            dbPlaylists = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        for appPlaylist in appPlaylists:
            if appPlaylist.id in dbPlaylists:
                dbPlaylist = dbPlaylists[appPlaylist.id]
                if (appPlaylist.link != dbPlaylist["url"]):
                    sqlService.update(table, appPlaylist.id, "url", f"\"{appPlaylist.link}\"")
                if (appPlaylist.title != dbPlaylist["title"]):
                    sqlService.update(table, appPlaylist.id, "title", f"\"{appPlaylist.title}\"")
                if (appPlaylist.description != dbPlaylist["description"]):
                    sqlService.update(table, appPlaylist.id, "description", f"\"{appPlaylist.description}\"")
                if (appPlaylist.createdBy != dbPlaylist["createdBy"]):
                    sqlService.update(table, appPlaylist.id, "createdBy", f"{appPlaylist.createdBy}")
                if (appPlaylist.createdAt != dbPlaylist["createdAt"]):
                    sqlService.update(table, appPlaylist.id, "createdAt", f"{appPlaylist.createdAt}")
                if (appPlaylist.updatedAt != dbPlaylist["updatedAt"]):
                    sqlService.update(table, appPlaylist.id, "updatedAt", f"{appPlaylist.updatedAt}")
            else:
                sqlService.create(table, "id, title, description, url, createdBy, createdAt, updatedAt", f"{appPlaylist.id}, \"{appPlaylist.title}\", \"{appPlaylist.description}\", \"{appPlaylist.link}\", {appPlaylist.createdBy}, {appPlaylist.createdAt}, {appPlaylist.updatedAt}")
        return

    @staticmethod
    def updateTags():
        from app.services import tagService as t
        appTags = t.TagService.allTags
        try:
            table = "Tag"
            dbTags = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        for appTag in appTags:
            if appTag.id in dbTags:
                dbTag = dbTags[appTag.id]
                if (appTag.title != dbTag["title"]):
                    sqlService.update(table, appTag.id, "title", f"\"{appTag.title}\"")
                if (appTag.createdAt != dbTag["createdAt"]):
                    sqlService.update(table, appTag.id, "createdAt", f"{appTag.createdAt}")
            else:
                sqlService.create(table, "id, title, createdAt", f"{appTag.id}, \"{appTag.title}\", {appTag.createdAt}")
        return

    @staticmethod
    def updateVotes():
        from app.services import voteService as v
        appVotes = v.VoteService.allVotes
        try:
            table = "Votes"
            dbVotes = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        for appVote in appVotes:
            if appVote.id in dbVotes:
                dbVote = dbVotes[appVote.id]
                if (appVote.uid != dbVote["uid"]):
                    sqlService.update(table, dbVote.id, "uid", f"{appVote.uid}")
                if (appVote.pid != dbVote["pid"]):
                    sqlService.update(table, dbVote.id, "pid", f"{appVote.pid}")
                if (appVote.tid != dbVote["tid"]):
                    sqlService.update(table, dbVote.id, "tid", f"{appVote.tid}")
                if (appVote.voteValue != dbVote["value"]):
                    sqlService.update(table, dbVote.id, "value", f"{appVote.voteValue}")
                if (appVote.createdAt != dbVote["createdAt"]):
                    sqlService.update(table, dbVote.id, "createdAt", f"{appVote.createdAt}")
                if (appVote.updatedAt != dbVote["updatedAt"]):
                    sqlService.update(table, dbVote.id, "updatedAt", f"{appVote.updatedAt}")
            else:
                sqlService.create(table, "id, uid, tid, pid, value, createdAt, updatedAt", f"{appVote.id}, {appVote.uid}, {appVote.tid}, {appVote.pid}, {appVote.voteValue}, {appVote.createdBy}, {appVote.createdAt}, {appVote.updatedAt}")
        return

    @staticmethod
    def updatePlaylistTags():
        from app.services import playlistService as p
        playlists = p.PlaylistService.allPlaylists
        appPlaylistTags = []

        print(playlists)

        for playlist in playlists:
            for tagID in playlist.tags:
                appPlaylistTags.append({"pid": playlist.id, "tid": tagID})

        try:
            table = "TagPlaylist_Relationship"
            dbPlaylistTags = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")

        for appPlaylistTag in appPlaylistTags:
            _pid, _tid = appPlaylistTag["pid"], appPlaylistTag["tid"]
            existing_entry = next(
                (entry for entry in dbPlaylistTags.values() if entry["pid"] == _pid and entry["tid"] == _tid),
                None
            )
            print(f"{_tid}, {_pid}, {existing_entry}")

            if existing_entry is None:
                sqlService.create(table, "pid, tid", f"{_pid}, {_tid}")

        return


    
    @staticmethod
    def deleteTrashBinItems():
        #TODO:
        return
    
    @staticmethod
    def readDB():
        sqlService.readUsers()
        sqlService.readPlaylists()
        sqlService.readTags()
        sqlService.readVotes()
        sqlService.readPlaylistTags()
    
    @staticmethod
    def readUsers():
        #TODO:
        return
    
    @staticmethod
    def readPlaylists():
        #TODO:
        return
    
    @staticmethod
    def readTags():
        #TODO:
        return
    
    @staticmethod
    def readVotes():
        #TODO:
        return
    
    @staticmethod
    def readPlaylistTags():
        #TODO:
        return
    

sqlService.init()
sqlService.updateDB()
