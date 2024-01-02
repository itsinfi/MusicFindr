from datetime import datetime
from app.models import playlistModel as p

class PlaylistService:
    allPlaylists = []

    #für testen only!!!
    @staticmethod
    def _createPlaylist(id: int, link: str, title: str, description: str, tagStrings: list[str], createdBy: datetime, createdAt: datetime, updatedAt: datetime):
        if (PlaylistService.playlistExists(id)):
            print(f"playlist already exists")
            return
        
        playlist = p.PlaylistModel(id, link, title, description, createdBy, createdAt, updatedAt)
        PlaylistService.allPlaylists.append(playlist)
        PlaylistService.updateTags(id, tagStrings)
        print(PlaylistService.allPlaylists)
        return
    
    @staticmethod
    def createPlaylist(link: str, title: str, description: str, tagStrings: list[str], createdBy: datetime):
        #if (not PlaylistService.linkExists(link)):

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
            id = 1
            while (PlaylistService.playlistExists(id)):
                id += 1

            playlist = p.PlaylistModel(id, link, title, description, createdBy, datetime.now(), datetime.now())
            PlaylistService.allPlaylists.append(playlist)
            PlaylistService.updateTags(id, tagStrings)
            print(PlaylistService.allPlaylists)
            # else:
            # print(f"playlist could not be created")
            return
    
    @staticmethod
    def readPlaylist(id: int) -> p.PlaylistModel:
        for playlist in PlaylistService.allPlaylists:
            if playlist.id == id:
                print(playlist)
                return playlist
        else:
            print(f"playlist with id {id} not found")

    def containsTag(id: int, tid: int) -> bool:
        from app.services import tagService as tag
        playlist = PlaylistService.readPlaylist(id)
        
        if playlist is None:
            print("Playlist does not exist!!!")
            return
        
        for _tid in playlist.tags:
            if (_tid == tid):
                print (f"Tag mit id {tid} in Playlist mit id {id} gefunden!")
                return True
        
        print (f"Tag mit id {tid} in Playlist mit id {id} nicht gefunden!")
        return False
    
    @staticmethod
    def playlistExists(id: int) -> bool:
        for playlist in PlaylistService.allPlaylists:
            if playlist.id == id:
                print(playlist)
                return True
        else:
            print(f"playlist with id {id} not found")
            return False

    @staticmethod
    def linkExists(link: str) -> bool:
        for playlist in PlaylistService.allPlaylists:
            if playlist.link == link:
                print(playlist)
                return True
        else:
            print(f"playlist with link {link} not found")
            return False

    @staticmethod
    def updatePlaylist(id: int, link: str, title: str, description: str, tagStrings: list[str]):
        playlist = PlaylistService.readPlaylist(id)
        if playlist is None:
            print("Playlist existiert nicht!")
            return
        
        playlist.link = link
        playlist.title = title
        playlist.description = description
        PlaylistService.updateTags(playlist.id, tagStrings)
        print(PlaylistService.allPlaylists)
        return
    
    #tagTitles bitte als Stringliste reingeben
    @staticmethod
    def updateTags(id: int, tagTitles : list[str]):
        from app.services import tagService as tag

        playlist = PlaylistService.readPlaylist(id)
        if playlist is None:
            print("Playlist existiert nicht!")
            return
        
        tags = []
        for tagTitle in tagTitles:
            tag.TagService.createTag(tagTitle)
            _t = tag.TagService.findTag(tagTitle)
            tags.append(_t.id)

        playlist.tags = tags
        print(PlaylistService.allPlaylists)
        return
    
    @staticmethod
    def deletePlaylist(id: int):
        from app.services import vote
        playlist = PlaylistService.readPlaylist(id)
        if playlist is None:
            print("Playlist existiert nicht!")
            return
        
        vote.VoteService.deleteAllPlaylistVotes(id) #alle verbundenen Votes löschen
        PlaylistService.allPlaylists.remove(playlist)
        print(f"Deleted playlist with id {id}")
        print(PlaylistService.allPlaylists)

    @staticmethod
    def removeTagFromAllPlaylists(tid: int):
        from app.services import tagService
        for playlist in PlaylistService.allPlaylists:
            if (PlaylistService.containsTag(playlist.id, tid)):
                playlist.tags.remove(tid)
                print(f"Deleted Tag with id {tid} from playlist with id {playlist.id}")
        return
    
    @staticmethod
    def deleteAllUserPlaylists(uid: int):
        for playlist in PlaylistService.allPlaylists:
            if (playlist.createdBy == uid):
                PlaylistService.deletePlaylist(playlist.id)
                print(f"Deleted Playlist with id {playlist.id} connected to user with id {uid}")
        return
    
