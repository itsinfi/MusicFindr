from datetime import datetime
from app.models import userModel as u
from bcrypt import _bcrypt

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

    #only for testing
    @staticmethod
    def _createUser(id: int, password: str, username: str, createdAt: datetime, updatedAt: datetime):
        """
        erstellt einen Nutzer (bitte nur für Testzwecke nutzen)\n
        throws UserServiceError if:
        - user id already exists
        - username already exists
        """

        #Prüfung, ob User-ID bereits existiert
        if UserService.userExists(id):
            raise UserServiceError(f"User with id {id} already exists.")

        #Prüfung, ob Username bereits 
        if UserService.usernameExists(username):
            raise UserServiceError(f"User with username {username} already exists.")

        #User wird erstellt
        user = u.UserModel(id, UserService.hashPassword(password), username, createdAt, updatedAt)

        #Hinzufügen zur User List
        UserService.allUsers.append(user)
        return
    

    @staticmethod
    def createUser(password: str, username: str):
        """
        erstellt einen Nutzer\n
        throws UserServiceError if:
        - username already exists
        """

        #Prüfung, ob Username bereits 
        if UserService.usernameExists(username):
            raise UserServiceError(f"User with username {username} already exists.")

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (UserService.userExists(id)):
            id += 1

        #User wird erstellt
        user = u.UserModel(id, UserService.hashPassword(password), username, datetime.now(), datetime.now())

        #User wird zur User List hinzugefügt
        UserService.allUsers.append(user)
        return
    

    @staticmethod
    def hashPassword(password: str) -> bytes:
        """
        hasht ein Passwort
        """
        return _bcrypt.hashpw(password.encode('utf-8'), _bcrypt.gensalt())
    

    @staticmethod
    def checkPassword(password: str, hashedPassword: str) -> bool:
        """
        checkt einen String mit einem gehashten Passwort gegen
        """
        return _bcrypt.checkpw(password.encode('utf-8'), hashedPassword)
    
    
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
        else:
            raise UserServiceError(f"User with id {id} could not be found or does not exist.")
        

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
        else:
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
        else:
            return False
    

    @staticmethod
    def updateUser(id: int, password: str, username: str):
        """
        updated die Daten eines Users\n
        throws UserServiceError if:
        - user with specified id does not exist
        """

        #User wird ausgelesen (+ Prüfung, ob User existiert)
        user = UserService.readUser(id)
        
        #User Daten werden geupdatet
        user.password = UserService.hashPassword(password)
        user.username = username

        #TODO: kann später entfernt werden, wird von der Datenbank übernommen
        user.updatedAt = datetime.now()
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

        #User wird ausgelesen (+ Prüfung, ob User existiert)
        user = UserService.readUser(id)
        
        #Votes des Users werden gelöscht
        vote.VoteService.deleteAllUserVotes(id)

        #Playlists des Users werden gelöscht
        playlist.PlaylistService.deleteAllUserPlaylists(id)

        #User wird gelöscht
        UserService.allUsers.remove(user)
        return