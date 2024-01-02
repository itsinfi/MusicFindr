from datetime import datetime
from app.models import voteModel as v

class VoteService:
    allVotes = []

    #für testen only!!!
    @staticmethod
    def _createVote(id, uid: int, pid: int, tid: int, voteValue: int, createdAt: datetime, updatedAt: datetime):
        from app.models import playlistModel as p
        from app.services import playlistService as _playlist
        from app.models import userModel as u
        from app.services import userService as _user
        from app.models import tagModel as t
        from app.services import tagService as _tag

        #wird automatisch gelöscht falls voteValue = 0
        if (voteValue == 0):
            VoteService.deleteVote(id)
            return
        
        if (VoteService.voteIDExists(id) or VoteService.voteExists(uid, pid, tid)):
            print(f"vote already exists")
            return
        
        if (not (voteValue == 1 or voteValue == -1)):
            print("Ungültiger Wert für den Vote!")
            return
        
        playlist = _playlist.PlaylistService.readPlaylist(pid)
        if (playlist is None):
            print("Playlist existiert nicht!")
            return
        
        user = _user.UserService.readUser(uid)
        if (user is None):
            print("User existiert nicht!")
            return
        
        tag = _tag.TagService.readTag(tid)
        if (tag is None):
            print("Tag existiert nicht!")
            return
        
        if (not _playlist.PlaylistService.containsTag(pid, tid)):
            print("Tag ist nicht kategorisiert zur Playlist!")
            return
        
        vote = v.VoteModel(id, uid, pid, tid, voteValue, createdAt, updatedAt)
        VoteService.allVotes.append(vote)
        print(VoteService.allVotes)
        return
    
    @staticmethod
    def createVote(uid: int, pid: int, tid: int, voteValue: int):
        from app.models import playlistModel as p
        from app.services import playlistService as _playlist
        from app.models import userModel as u
        from app.services import userService as _user
        from app.models import tagModel as t
        from app.services import tagService as _tag

        #wird automatisch gelöscht falls voteValue = 0
        if (voteValue == 0):
            vote = VoteService.findVote(uid, pid, tid)
            print(vote.id)
            if vote is not None:
                VoteService.deleteVote(vote.id)
                return
        
        if (VoteService.voteExists(uid, pid, tid)):
            print(f"vote already exists")
            return
        
        if (not (voteValue == 1 or voteValue == -1)):
            print("Ungültiger Wert für den Vote!")
            return
        
        playlist = _playlist.PlaylistService.readPlaylist(pid)
        if (playlist is None):
            print("Playlist existiert nicht!")
            return
        
        user = _user.UserService.readUser(uid)
        if (user is None):
            print("User existiert nicht!")
            return
        
        tag = _tag.TagService.readTag(tid)
        if (tag is None):
            print("Tag existiert nicht!")
            return
        
        if (not _playlist.PlaylistService.containsTag(pid, tid)):
            print("Tag ist nicht kategorisiert zur Playlist!")
            return

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (VoteService.voteIDExists(id)):
            id += 1

        vote = v.VoteModel(id, uid, pid, tid, voteValue, datetime.now(), datetime.now())
        VoteService.allVotes.append(vote)
        print(VoteService.allVotes)
        return
    
    @staticmethod
    def readVote(id: int) -> v.VoteModel:
        for vote in VoteService.allVotes:
            if vote.id == id:
                print(vote)
                return vote
        else:
            print(f"vote with id {id} not found")
            return

    @staticmethod
    def findVote(uid: int, pid: int, tid: int) -> v.VoteModel:
        for vote in VoteService.allVotes:
            if (vote.uid == uid and vote.pid == pid and vote.tid == tid):
                print(vote)
                return vote
        else:
            print(f"Vote does not exist so far!")
            return

    @staticmethod
    def voteIDExists(id: int) -> bool:
        for vote in VoteService.allVotes:
            if vote.id == id:
                print(vote)
                return True
        else:
            print(f"vote with id {id} not found")
            return False

    @staticmethod
    def voteExists(uid: int, pid: int, tid: int) -> bool:
        for vote in VoteService.allVotes:
            if (vote.uid == uid and vote.pid == pid and vote.tid == tid):
                print(vote)
                return True
        else:
            print(f"Vote does not exist so far!")
            return False
    
    @staticmethod
    def updateVote(id: int, value: int):
        vote = VoteService.readVote(id)
        if vote is None:
            print(f"Vote with id {id} does not exist!")
            return
        
        if (value == 0):
            VoteService.deleteVote(id)
            return
        
        vote.value = value
        print(VoteService.allVotes)   
        return
    
    @staticmethod
    def deleteVote(id: int):
        vote = VoteService.readVote(id)
        if vote is None:
            print(f"Vote with id {id} does not exist!")
            return
        
        VoteService.allVotes.remove(vote)
        print(f"Deleted vote with id {id}")
        print(VoteService.allVotes)   
        return
    
    @staticmethod
    def deleteAllPlaylistVotes(pid: int):
        for vote in VoteService.allVotes:
            if (vote.pid == pid):
                VoteService.deleteVote(vote.id)
                print(f"Deleted Vote with id {vote.id} connected to playlist with id {pid}")
        return

    @staticmethod
    def deleteAllTagVotes(tid: int):
        for vote in VoteService.allVotes:
            if (vote.tid == tid):
                print(f"Deleted Vote with id {vote.id} connected to tag with id {tid}")
        return

    @staticmethod
    def deleteAllUserVotes(uid: int):
        for vote in VoteService.allVotes:
            if (vote.uid == uid):
                print(f"Deleted Vote with id {vote.id} connected to user with id {uid}")
        return
        
        
