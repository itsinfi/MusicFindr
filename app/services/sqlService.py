from threading import Lock
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

    # trashBin = []

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
    def delete(tableName:str, id:int):
        with sqlService.engine.connect() as connection:
            query = text(f"DELETE FROM {tableName} WHERE id = {id};")
            connection.execute(query)
            connection.commit()
    
    @staticmethod
    def deleteAllContainingID(tableName:str, idName: str, id:int):
        with sqlService.engine.connect() as connection:
            query = text(f"DELETE FROM {tableName} WHERE {idName} = {id};")
            # print(query)
            connection.execute(query)
            connection.commit()

    # @staticmethod
    # def trash(item):
    #     sqlService.trashBin.append(item)

    @staticmethod
    def insertIntoTable(tableName: str, columnValues: dict):
        print("bjjnsnjsjnjnjnjgninjgnijninnnjj")
        with sqlService.engine.connect() as connection:
            # Generate column names and placeholders from the dictionary
            columns = ', '.join(columnValues.keys())
            placeholders = ', '.join(f':{col}' for col in columnValues.keys())

            # Construct the SQL query
            query = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})"

            # Execute the prepared statement with parameter values
            connection.execute(text(query), columnValues)
            connection.commit()

    @staticmethod
    def updateTable(tableName: str, id:int, columnValues: dict):
        del columnValues["id"]
        with sqlService.engine.connect() as connection:
            # Generate SET clause for the UPDATE statement
            set_clause = ', '.join(f'{col} = :{col}' for col in columnValues.keys())

            # Construct the SQL query with a WHERE clause based on the id parameter
            query = f"UPDATE {tableName} SET {set_clause} WHERE id = :id"

            # Add the id parameter to the columnValues dictionary
            columnValues['id'] = id

            # Execute the prepared statement with parameter values
            connection.execute(text(query), columnValues)
            connection.commit()
  
    @staticmethod
    def updateDB():
        sqlService.updateVotes()
        sqlService.updateTags()
        sqlService.updatePlaylistTags()
        sqlService.updatePlaylists()
        sqlService.updateUsers()

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
            appUserDict = {
                "id"        :   appUser.id,
                "username"  :   appUser.username,
                "password"  :   appUser.password,
                "createdAt" :   appUser.createdAt,
                "updatedAt" :   appUser.updatedAt
            }

            if not( appUser.id in dbUsers ):
                sqlService.insertIntoTable("User", appUserDict)
                continue

            dbUser = dbUsers[appUser.id]
            dbUserDict = {
                "id"        :   dbUser["id"],
                "username"  :   dbUser["username"],
                "password"  :   dbUser["password"],
                "createdAt" :   dbUser["createdAt"],
                "updatedAt" :   dbUser["updatedAt"]
            }

            if not( dbUserDict == appUserDict ):
                #print("USer Data to sync:")
                #print("db:  "+dbUserDict)
                #print("app: "+appUserDict)
                sqlService.updateTable("User", dbUserDict["id"], appUserDict)
                continue

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
            appPlaylistDict = {
                "id"            :   appPlaylist.id,
                "title"         :   appPlaylist.title,
                "description"    :   appPlaylist.description,
                "link"          :   appPlaylist.link,
                "createdBy"     :   appPlaylist.createdBy,
                "createdAt"     :   appPlaylist.createdAt,
                "updatedAt"     :   appPlaylist.updatedAt
            }

            if not( appPlaylist.id in dbPlaylists ):
                sqlService.insertIntoTable("Playlist", appPlaylistDict)
                continue

            dbPlaylist = dbPlaylists[appPlaylist.id]
            dbPlaylistDict = {
                "id"            :   dbPlaylist["id"],
                "title"         :   dbPlaylist["title"],
                "decription"    :   dbPlaylist["description"],
                "link"          :   dbPlaylist["link"],
                "createdBy"     :   dbPlaylist["createdBy"],
                "createdAt"     :   dbPlaylist["createdAt"],
                "updatedAt"     :   dbPlaylist["updatedAt"]
            }

            if not( dbPlaylistDict == appPlaylistDict ):
                #print("Playlist Data to sync:")
                #print(f"db:     {dbPlaylistDict}")
                #print(f"app:    {appPlaylistDict}")
                sqlService.updateTable("Playlist", dbPlaylistDict["id"], appPlaylistDict)
                continue
        
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
            appTagDict = {
                "id"            :   appTag.id,
                "title"         :   appTag.title,
                "createdAt"     :   appTag.createdAt
            }

            if not( appTag.id in dbTags ):
                sqlService.insertIntoTable("Tag", appTagDict)
                continue

            dbTag = dbTags[appTag.id]
            dbTagDict = {
                "id"            :   dbTag["id"],
                "title"         :   dbTag["title"],
                "createdAt"     :   dbTag["createdAt"]
            }

            if not( dbTagDict == appTagDict ):
                #print("Playlist Data to sync:")
                #print("db:  "+dbTagDict)
                #print("app: "+appTagDict)
                sqlService.updateTable("Tag", dbTagDict["id"], appTagDict)
                continue
        
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
            appVoteDict = {
                "id"            :   appVote.id,
                "uid"           :   appVote.uid,
                "tid"           :   appVote.tid,
                "pid"           :   appVote.pid,
                "value"         :   appVote.voteValue,
                "createdAt"     :   appVote.createdAt,
                "updatedAt"     :   appVote.updatedAt
            }

            if not( appVote.id in dbVotes ):
                sqlService.insertIntoTable("Votes", appVoteDict)
                continue

            dbVote = dbVotes[appVote.id]
            dbVoteDict = {
                "id"            :   dbVote["id"],
                "uid"           :   dbVote["uid"],
                "tid"           :   dbVote["tid"],
                "pid"           :   dbVote["pid"],
                "value"         :   dbVote["value"],
                "createdAt"     :   dbVote["createdAt"],
                "updatedAt"     :   dbVote["updatedAt"]
            }

            if not( dbVoteDict == appVoteDict ):
                #print("Vote Data to sync:")
                #print("db:  "+dbVoteDict)
                #print("app: "+appVoteDict)
                sqlService.updateTable("Votes", dbVoteDict["id"], appVoteDict)
                continue
        
        return

    @staticmethod
    def updatePlaylistTags():
        from app.services import playlistService as p
        playlists = p.PlaylistService.allPlaylists
        appPlaylistTags = []

        # print(playlists)

        for playlist in playlists:
            for tagID in playlist.tags:
                appPlaylistTags.append({"pid": playlist.id, "tid": tagID})
        
        # print(playlists)

        try:
            table = "TagPlaylist_Relationship"
            dbPlaylistTags = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        # print(appPlaylistTags)
        for appPlaylistTag in appPlaylistTags:
            _pid, _tid = appPlaylistTag["pid"], appPlaylistTag["tid"]
            existing_entry = next(
                (entry for entry in dbPlaylistTags.values() if entry["pid"] == _pid and entry["tid"] == _tid),
                None
            )
            # print(f"{_tid}, {_pid}, {existing_entry}")

            if existing_entry is None:
                sqlService.create(table, "pid, tid", f"{_pid}, {_tid}")
            

        return
    
    # @staticmethod
    # def deleteTrashBinItems():
    #     return
    
    @staticmethod
    def readDB():
        sqlService.readUsers()
        sqlService.readPlaylists()
        sqlService.readTags()
        sqlService.readVotes()
        sqlService.readPlaylistTags()
    
    @staticmethod
    def readUsers():
        from app.services import userService as u
        try:
            table = "User"
            dbUsers = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        for id, dbUser in dbUsers.items():
            # print(dbUser)
            try:
                u.UserService._createUser(int(dbUser["id"]), dbUser["password"], dbUser["username"], int(dbUser["createdAt"]), int(dbUser["updatedAt"]))
            except Exception as e:
                print(e)
                continue
        # print(u.UserService.allUsers)
        return
    
    @staticmethod
    def readPlaylists():
        from app.services import playlistService as p
        try:
            table = "Playlist"
            dbPlaylists = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        for id, dbPlaylist in dbPlaylists.items():
            # print(dbPlaylist)
            try:
                p.PlaylistService._createPlaylist(int(dbPlaylist["id"]), dbPlaylist["link"], dbPlaylist["title"], dbPlaylist["description"], [], int(dbPlaylist["createdBy"]), int(dbPlaylist["createdAt"]), int(dbPlaylist["updatedAt"]))
            except Exception as e:
                print(e)
                continue
        # print(p.PlaylistService.allPlaylists)
        return
    
    @staticmethod
    def readTags():
        from app.services import tagService as t
        try:
            table = "Tag"
            dbTags = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        for id, dbTag in dbTags.items():
            # print(dbTag)
            try:
                t.TagService._createTag(int(dbTag["id"]), dbTag["title"], int(dbTag["createdAt"]))
            except Exception as e:
                print(e)
                continue
        return
    
    @staticmethod
    def readVotes():
        from app.services import voteService as v
        try:
            table = "Votes"
            dbVotes = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        for id, dbVote in dbVotes.items():
            # print(dbTag)
            try:
                v.VoteService._createVote(int(dbVote["id"]), int(dbVote["uid"]), int(dbVote["pid"]), int(dbVote["tid"]), int(dbVote["value"]), int(dbVote["createdAt"]), int(dbVote["updatedAt"]))
            except Exception as e:
                print(e)
                continue
        return
    
    @staticmethod
    def readPlaylistTags():
        from app.services import playlistService as p
        try:
            table = "TagPlaylist_Relationship"
            dbPlaylistTags = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        try:
            table = "Playlist"
            dbPlaylists = sqlService.read(table)
        except Exception as e:
            raise sqlServiceError(f"The table {table} could not be found or does not exist.")
        
        for dbPlaylist in dbPlaylists.values():
            playlistTags = []
            for dbPlaylistTag in dbPlaylistTags.values():
                if (dbPlaylist["id"] == dbPlaylistTag["pid"]):
                    playlistTags.append(dbPlaylistTag["tid"])
            try:
                playlist = p.PlaylistService.readPlaylist(dbPlaylist["id"])
                playlist.tags = playlistTags
            except Exception as e:
                print(e)
                continue
        return
    

sqlService.init()
