from datetime import datetime
from app.models import voteModel as v

class VoteServiceError(Exception):
    """
    Custom Error Klasse für Methoden des VoteService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class VoteService:
    allVotes = []


    #only for testing
    @staticmethod
    def _createVote(id, uid: int, pid: int, tid: int, voteValue: int, createdAt: datetime, updatedAt: datetime):
        """
        erstellt einen Vote (bitte nur für Testzwecke nutzen)\n
        throws VoteServiceException if:
        - voteValue is not -1 or 1
        - playlist, tag or user does not exist
        - tag is not assigned to playlist tags
        - vote with same id already exists
        """
        from app.models import playlistModel as p
        from app.services import playlistService as _playlist
        from app.models import userModel as u
        from app.services import userService as _user
        from app.models import tagModel as t
        from app.services import tagService as _tag

        #Vote wird automatisch gelöscht falls voteValue = 0
        if (voteValue == 0):
            try:
                VoteService.deleteVote(id)
                raise VoteServiceError(f"Deleted vote with id {id} because value was 0.")
            except VoteServiceError as e:
                print(e)
        
        #Prüfung, ob Vote-ID oder Kombi von pid, tid und uid bereits existiert
        if (VoteService.voteIDExists(id) or VoteService.voteExists(uid, pid, tid)):
            raise VoteServiceError(f"Vote already exists.")
        
        #Prüfung, ob Vote nicht Value 1 oder -1 ist
        if (not (voteValue == 1 or voteValue == -1)):
            raise VoteServiceError(f"Vote value can only be 1 or -1 and not {voteValue}.")
        

        #Prüfung, ob Playlist nicht existiert
        if not (_playlist.PlaylistService.playlistExists(pid)):
            raise VoteServiceError(f"Playlist with id {pid} could not be found or does not exist.")
        
        #Prüfung, ob User nicht existiert
        if not (_user.UserService.userExists(uid)):
            raise VoteServiceError(f"User with id {uid} could not be found or does not exist.")
        
        #Prüfung, ob Tag nicht existiert
        if not (_tag.TagService.tagExists(tid)):
            raise VoteServiceError(f"Tag with id {tid} could not be found or does not exist.")
        
        #Prüfung, ob der Tag nicht der Playlist hinzugefügt ist
        if not (_playlist.PlaylistService.containsTag(pid, tid)):
            raise VoteServiceError(f"Tag with id {tid} does not categorize playlist with id {pid}")
        
        #Vote erstellen
        vote = v.VoteModel(id, uid, pid, tid, voteValue, createdAt, updatedAt)

        #Vote zur Votelist hinzufügen
        VoteService.allVotes.append(vote)
        return
    

    @staticmethod
    def createVote(uid: int, pid: int, tid: int, voteValue: int):
        """
        erstellt einen Vote\n
        throws VoteServiceException if:
        - voteValue is not -1 or 1
        - playlist, tag or user does not exist
        - tag is not assigned to playlist tags
        """
        from app.models import playlistModel as p
        from app.services import playlistService as _playlist
        from app.models import userModel as u
        from app.services import userService as _user
        from app.models import tagModel as t
        from app.services import tagService as _tag

        # #Vote wird automatisch gelöscht falls voteValue = 0
        # if (voteValue == 0):
        #     try:
        #         VoteService.deleteVote(id)
        #         raise VoteServiceError(f"Deleted vote with id {id} because value was 0.")
        #     except VoteServiceError as e:
        #         print(e)
        
        #Prüfung, ob Kombi von pid, tid und uid bereits existiert
        if (VoteService.voteExists(uid, pid, tid)):
            raise VoteServiceError(f"Vote already exists.")
        
        #Prüfung, ob Vote nicht Value 1 oder -1 ist
        if (not (voteValue == 1 or voteValue == -1)):
            raise VoteServiceError(f"Vote value can only be 1 or -1 and not {voteValue}.")
        

        #Prüfung, ob Playlist nicht existiert
        if not (_playlist.PlaylistService.playlistExists(pid)):
            raise VoteServiceError(f"Playlist with id {pid} could not be found or does not exist.")
        
        #Prüfung, ob User nicht existiert
        if not (_user.UserService.userExists(uid)):
            raise VoteServiceError(f"User with id {uid} could not be found or does not exist.")
        
        #Prüfung, ob Tag nicht existiert
        if not (_tag.TagService.tagExists(tid)):
            raise VoteServiceError(f"Tag with id {tid} could not be found or does not exist.")
        
        #Prüfung, ob der Tag nicht der Playlist hinzugefügt ist
        if not (_playlist.PlaylistService.containsTag(pid, tid)):
            raise VoteServiceError(f"Tag with id {tid} does not categorize playlist with id {pid}")
        
        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (VoteService.voteIDExists(id)):
            id += 1

        #Vote erstellen
        vote = v.VoteModel(id, uid, pid, tid, voteValue, datetime.now(), datetime.now())
        
        #Vote zur Votelist hinzufügen
        VoteService.allVotes.append(vote)
        return
    
    
    @staticmethod
    def readVote(id: int) -> v.VoteModel:
        """
        gibt einen Vote mit der ID zurück, falls dieser existiert\n
        throws VoteServiceError if:
        - playlist with specified id does not exist
        """

        #Suchen nach Vote mit der ID
        for vote in VoteService.allVotes:
            if vote.id == id:
                return vote
            
        #VoteServiceError, falls nicht gefunden
        raise VoteServiceError(f"Vote with id {id} could not be found or does not exist.")


    #########DO WE NEED THIS??????
    # @staticmethod
    # def findVote(uid: int, pid: int, tid: int) -> v.VoteModel:
    #     for vote in VoteService.allVotes:
    #         if (vote.uid == uid and vote.pid == pid and vote.tid == tid):
    #             print(vote)
    #             return vote
    #     
    #     print(f"Vote does not exist so far!")
    #     return


    @staticmethod
    def voteIDExists(id: int) -> bool:
        """
        gibt true zurück, falls ein Vote mit der ID existiert\n
        """

        #Suchen nach Vote mit der id
        for vote in VoteService.allVotes:
            if vote.id == id:
                return True
            
        #Ansonsten false returnen
        return False


    @staticmethod
    def voteExists(uid: int, pid: int, tid: int) -> bool:
        """
        gibt true zurück, falls ein Vote mit der User id, Playlist id und Tag id existiert\n
        """

        #Suchen nach Vote mit uid, pid und tid
        for vote in VoteService.allVotes:
            if (vote.uid == uid and vote.pid == pid and vote.tid == tid):
                return True
            
        #Ansonsten false returnen
        return False
    

    @staticmethod
    def updateVote(id: int, voteValue: int):
        """
        updated die Daten eines Votes\n
        throws VoteServiceError if:
        - vote with specified id does not exist
        - vote value is not 1, 0 or -1
        """

        #Vote wird ausgelesen (+ Prüfung, ob Vote existiert)
        vote = VoteService.readVote(id)
        
        #Falls value = 0 ist, wird dieser gelöscht
        if (voteValue == 0):
            VoteService.deleteVote(id)
            return
        
        #Prüfung, ob voteValue Wert 1 oder -1 ist
        if not voteValue == 1 or voteValue == -1:
            raise VoteServiceError(f"Vote value can only be 1 or -1 and not {voteValue}.")
        
        #Vote Daten werden geupdatet
        vote.value = voteValue  

        #TODO: kann später entfernt werden, wird von der Datenbank übernommen
        vote.updatedAt = datetime.now()
        return
    

    @staticmethod
    def deleteVote(id: int):
        """
        löscht einen Vote\n
        throws VoteServiceError if:
        - vote with specified id does not exist
        """

        #Vote wird ausgelesen (+ Prüfung, ob Vote existiert)
        vote = VoteService.readVote(id)
        
        #Vote wird gelöscht
        VoteService.allVotes.remove(vote)
        return
    

    @staticmethod
    def deleteAllPlaylistVotes(pid: int):
        """
        löscht alle Votes einer Playlist\n
        """

        #Alle Votes der Playlist werden gesucht und gelöscht
        for vote in VoteService.allVotes:
            if (vote.pid == pid):
                try:
                    VoteService.deleteVote(vote.id)
                except VoteServiceError as e:
                    print(e)
                    continue
        return


    @staticmethod
    def deleteAllTagVotes(tid: int):
        """
        löscht alle Votes eines Tags\n
        """

        #Alle Votes des Tags werden gesucht und gelöscht
        for vote in VoteService.allVotes:
            if (vote.tid == tid):
                try:
                    VoteService.deleteVote(vote.id)
                except VoteServiceError as e:
                    print(e)
                    continue
        return


    @staticmethod
    def deleteAllUserVotes(uid: int):
        """
        löscht alle Votes eines Users\n
        """

        #Alle Votes des Users werden gesucht und gelöscht
        for vote in VoteService.allVotes:
            if (vote.uid == uid):
                try:
                    VoteService.deleteVote(vote.id)
                except VoteServiceError as e:
                    print(e)
                    continue
        return