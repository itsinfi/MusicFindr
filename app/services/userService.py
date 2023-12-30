from datetime import datetime
from app.models import userModel as u
from bcrypt import _bcrypt


class UserService:
    allUsers = []

    #für testen only!!!
    @staticmethod
    def _createUser(id: int, password: str, username: str, createdAt: datetime, updatedAt: datetime):
        if (UserService.userExists(id)):
            print(f"user already exists")
            return
            
        if (UserService.usernameExists(username)):
            print(f"username already exists")
            return
        
        user = u.UserModel(id, UserService.hashPassword(password), username, createdAt, updatedAt)
        UserService.allUsers.append(user)
        print(UserService.allUsers)
        return
    
    @staticmethod
    def createUser(password: str, username: str):
        if (UserService.usernameExists(username)):
            print(f"username already exists")

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (UserService.userExists(id)):
            id += 1

        user = u.UserModel(id, UserService.hashPassword(password), username, datetime.now(), datetime.now())
        UserService.allUsers.append(user)
        print(UserService.allUsers)
        return
    
    @staticmethod
    def hashPassword(password: str):
        return _bcrypt.hashpw(password.encode('utf-8'), _bcrypt.gensalt())
    
    @staticmethod
    def checkPassword(password: str, hashedPassword: str):
        return _bcrypt.checkpw(password.encode('utf-8'), hashedPassword)
    
    @staticmethod
    def readUser(id: int) -> u.UserModel:
        for user in UserService.allUsers:
            if user.id == id:
                print(user)
                return user
        else:
            print(f"user with id {id} not found")
            return

    @staticmethod
    def userExists(id: int) -> bool:
        for user in UserService.allUsers:
            if user.id == id:
                print(user)
                return True
        else:
            print(f"user with id {id} not found")
            return False

    @staticmethod
    def usernameExists(username: str) -> bool:
        for user in UserService.allUsers:
            if user.username == username:
                print(user)
                return True
        else:
            print(f"user with username {username} not found")
            return False
    
    @staticmethod
    def updateUser(id: int, password: str, username: str):
        user = UserService.readUser(id)
        if user is None:
            print("User does not exist!")
            return
        
        user.password = UserService.hashPassword(password)
        user.username = username
        user.updatedAt = datetime.now()
        print(UserService.allUsers)
        return
    
    #TODO: Redundanzen auslöschen (zu Tags, Votes und Playlists)
    @staticmethod
    def deleteUser(id: int):
        user = UserService.readUser(id)
        if user is None:
            print("User does not exist!")
            return
        
        UserService.allUsers.remove(user)
        print(UserService.allUsers)
        return