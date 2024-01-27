from datetime import datetime
import re
from app.models import userModel as u
from bcrypt import _bcrypt

from flask import session

class UserServiceError(Exception):
    """
    Custom Error Klasse für Methoden des UserService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class UserService:
    allUsers = []

    @staticmethod
    def checkCurrentUserIsLoggedIn() -> bool:
        if "username" in session:
            return True
        else:
            return False
        
    @staticmethod
    def getSessionUsername() -> str:
        if UserService.checkCurrentUserIsLoggedIn:
            return session["username"]
        else:
            return None

    #only for testing
    @staticmethod
    def _createUser(id: int, password: str, username: str, createdAt: int, updatedAt: int):
        # print("user created")
        """
        erstellt einen Nutzer (bitte nur für Testzwecke nutzen)\n
        throws UserServiceError if:
        - user id already exists
        - username already exists
        - username/password requirements are not fulfilled (individual error message)
        """

        #Prüfung, ob User-ID bereits existiert
        if UserService.userExists(id):
            raise UserServiceError(f"User with id {id} already exists.")

        #Prüfung, ob Username bereits existiert
        if UserService.usernameExists(username):
            raise UserServiceError(f"User with username {username} already exists.")

        #User wird erstellt
        user = u.UserModel(id, password, username, createdAt, updatedAt)

        #Hinzufügen zur User List
        UserService.allUsers.append(user)
        return
    

    @staticmethod
    def createUser(password: str, username: str):
        """
        erstellt einen Nutzer\n
        throws UserServiceError if:
        - username already exists
        - username/password requirements are not fulfilled (individual error message)
        """

        #Prüfung, ob Username bereits existiert
        if UserService.usernameExists(username):
            raise UserServiceError(f"User with username {username} already exists.")
        
        #Username checken
        UserService.validateUsername(username)

        #Password checken
        UserService.validatePassword(password)

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (UserService.userExists(id)):
            id += 1

        #User wird erstellt
        user = u.UserModel(id, UserService.hashPassword(password), username, int(datetime.now().timestamp()), int(datetime.now().timestamp()))

        #User wird zur User List hinzugefügt
        UserService.allUsers.append(user)
        return
    
    @staticmethod
    def login(password: str, username: str):
        errorMessage = "Wrong username or password."

        if (UserService.usernameExists(username)):
            user = UserService.getUserViaUsername(username)
            if UserService.checkPassword(password, user.password.encode()):
                # log in
                session["userId"] = user.id
                session["username"] = user.username
            else:
                raise UserServiceError(errorMessage)
        else:
            raise UserServiceError(errorMessage)

    @staticmethod
    def logout():
        if "username" in session:
            # session["username"] = None
            # session["userId"] = None
            # session.clear

            session.pop("username")
            session.pop("userId")

    @staticmethod
    def hashPassword(password: str) -> bytes:
        """
        hasht ein Passwort
        """
        return _bcrypt.hashpw(password.encode('utf-8'), _bcrypt.gensalt()).decode()
    

    @staticmethod
    def checkPassword(password: str, hashedPassword: str) -> bool:
        """
        checkt einen String mit einem gehashten Passwort gegen
        """
        return _bcrypt.checkpw(password.encode('utf-8'), hashedPassword)
    

    @staticmethod
    def validateUsername(username: str) -> bool:
        """
        checks an username for the following criteria\n
        (throws an UserServiceException if not fulfilled):
        - not empty
        - at least 3 character long
        - maximum of 20 characters long
        - only contains letters (a-z, A-Z), numbers and underscores
        """

        #Error String (erstmal leer)
        error = ""

        #Checken, ob der Username leer ist
        if not len(username) > 0:
            error += "- The username is empty. The field is required."
        
        #Checken, ob der Username zu kurz ist
        if not len(username) >= 3:
            if error:
                error += "<br>"
            error += "- The username is too short. At least 3 characters are required."

        #Checken, ob der Username zu lang ist
        if not len(username) <= 20:
            if error:
                error += "<br>"
            error+= "- The username is too long. It can be no more than 20 characters long."
        
        #Characters checken
        regex = r"^[a-zA-Z0-9_]+$"
        if not (re.match(regex, username)):
            if error:
                error += "<br>"
            error += "- The username contains invalid characters. Allowed are only small letters, numbers and underscores."
        
        #Falls der Error String nicht leer ist, den Error raisen
        if error:
            raise UserServiceError(error)
        
        #Anforderungen erfüllt
        return True
    

    @staticmethod
    def validatePassword(password: str) -> bool:
        """
        checks a password for the following criteria\n
        (throws an UserServiceException if not fulfilled):
        - not empty
        - at least 6 character long
        """

        #Error String (erstmal leer)
        error = ""

        #Checken, ob das Passwort leer ist
        if not len(password) > 0:
            error += "The password is empty. The field is required."
        
        #Checken, ob das Passwort zu kurz ist
        if not len(password) >= 6:
            if error:
                error += "<br>"
            error += "The password is too short. At least 6 characters are required."
        
        #Falls der Error String nicht leer ist, den Error raisen
        if error:
            raise UserServiceError(error)
        
        #Anforderungen erfüllt
        return True
    
    
    @staticmethod
    def readUser(id: int) -> u.UserModel:
        """
        gibt einen User der ID zurück, falls dieser existiert\n
        throws UserServiceError if:
        - user with specified id does not exist
        """

        #Suchen nach User mit der ID
        for user in UserService.allUsers:
            if user.id == id:
                return user
        
        #UserServiceError, falls nicht gefunden
        raise UserServiceError(f"User with id {id} could not be found or does not exist.")
    
    @staticmethod
    def getUserViaUsername(username: str) -> u.UserModel:
        for user in UserService.allUsers:
            if user.username == username:
                return user
        

    @staticmethod
    def userExists(id: int) -> bool:
        """
        prüft, ob ein Nutzer unter der ID bereits existiert
        """

        #Suchen nach User mit der ID
        for user in UserService.allUsers:
            if user.id == id:
                return True
            
        #Ansonsten false returnen
        return False
        
    
    @staticmethod
    def usernameExists(username: str) -> bool:
        """
        prüft, ob ein Nutzername bereits existiert
        """

        #Suchen nach Nutzer mit Nutzernamen
        for user in UserService.allUsers:
            if user.username == username:
                return True
        
        #Ansonsten false returnen
        return False
    

    @staticmethod
    def updateUser(id: int, password: str, username: str):
        """
        updated die Daten eines Users\n
        throws UserServiceError if:
        - user with specified id does not exist
        - username/password requirements are not fulfilled (individual error message)
        """
        
        #Username checken
        UserService.validateUsername(username)

        #Password checken
        UserService.validatePassword(password)

        #User wird ausgelesen (+ Prüfung, ob User existiert)
        user = UserService.readUser(id)

        #Prüfung, ob Username bereits existiert, falls dieser geändert werden soll
        if (user.username != username and UserService.usernameExists(username)):
            raise UserServiceError(f"User with username {username} already exists.")
        
        #User Daten werden geupdatet
        # if not (UserService.checkPassword(password)):
        #     user.password = UserService.hashPassword(password)

        if (user.username != username):
            user.username = username

        #TODO: kann später entfernt werden, wird von der Datenbank übernommen
        user.updatedAt = int(datetime.now().timestamp())
        return
    

    @staticmethod
    def deleteUser(id: int):
        """
        löscht einen Nutzer + alle Playlists und Votes des Nutzers\n
        throws UserServiceError if:
        - user with specified id does not exist
        """
        from app.services import playlist
        from app.services import vote
        from app.services import sqlService as sql

        #User wird ausgelesen (+ Prüfung, ob User existiert)
        user = UserService.readUser(id)
        
        #Votes des Users werden gelöscht
        vote.VoteService.deleteAllUserVotes(id)

        #Playlists des Users werden gelöscht
        playlist.PlaylistService.deleteAllUserPlaylists(id)

        #User wird gelöscht
        UserService.allUsers.remove(user)

        #User wird aus der DB gelöscht
        sql.sqlService.delete("User", id)
        return