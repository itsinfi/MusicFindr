from datetime import datetime
from app.models import playlistModel as p

class PlaylistServiceError(Exception):
    """
    Custom Error Klasse für Methoden des PlaylistService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class PlaylistService:
    allPlaylists = []


    #only for testing
    @staticmethod
    def _createPlaylist(id: int, link: str, title: str, description: str, tagStrings: list[str], createdBy: datetime, createdAt: datetime, updatedAt: datetime):
        """
        erstellt eine Playlist (bitte nur für Testzwecke nutzen)\n
        throws PlaylistServiceException if:
        - playlist with id already exists
        """

        #Prüfung, ob Playlist-ID bereits existiert
        if (PlaylistService.playlistExists(id)):
            raise PlaylistServiceError(f"Playlist with id {id} already exists.")
        
        #Playlist erstellen
        playlist = p.PlaylistModel(id, link, title, description, createdBy, createdAt, updatedAt)

        #Playlist zur Playlist list hinzufügen
        PlaylistService.allPlaylists.append(playlist)

        #Tags der Playlist hinzufügen
        try:
            PlaylistService.updateTags(id, tagStrings)
        except PlaylistServiceError as e:
            raise PlaylistServiceError(f"Etwas ist beim Hinzufügen der Tags schief gelaufen.")
        return
    

    @staticmethod
    def createPlaylist(link: str, title: str, description: str, tagStrings: list[str], createdBy: datetime):
        """
        erstellt eine Playlist\n
        """
        #if (not PlaylistService.linkExists(link)):

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (PlaylistService.playlistExists(id)):
            id += 1

        #Playlist erstellen
        playlist = p.PlaylistModel(id, link, title, description, createdBy, datetime.now(), datetime.now())

        #Playlist zur Playlist list hinzufügen
        PlaylistService.allPlaylists.append(playlist)
        
        #Tags der Playlist hinzufügen
        try:
            PlaylistService.updateTags(id, tagStrings)
        except PlaylistServiceError as e:
            raise PlaylistServiceError(f"Etwas ist beim Hinzufügen der Tags schief gelaufen.")

        # print(f"playlist could not be created")
        return
    

    @staticmethod
    def readPlaylist(id: int) -> p.PlaylistModel:
        """
        gibt eine Playlist der ID zurück, falls diese existiert\n
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """

        #Suchen nach Playlist mit der ID
        for playlist in PlaylistService.allPlaylists:
            if playlist.id == id:
                return playlist
            
        #PlaylistServiceError, falls nicht gefunden
        raise PlaylistServiceError(f"Playlist with id {id} could not be found or does not exist.")


    def containsTag(id: int, tid: int) -> bool:
        """
        gibt true zurück, falls das Tag mit der tid in der Playlist mit der id existiert\n
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """
        from app.services import tagService as tag

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)
        
        #Suchen nach Tag mit id in den Tags der Playlist
        for _tid in playlist.tags:
            if (_tid == tid):
                return True
        
        #Ansonsten false returnen
        return False
    

    @staticmethod
    def playlistExists(id: int) -> bool:
        """
        gibt true zurück, falls eine Playlist mit der ID existiert\n
        """

        #Suchen nach Playlist mit ID
        for playlist in PlaylistService.allPlaylists:
            if playlist.id == id:
                return True
            
        #Ansonsten false returnen
        return False

    
    @staticmethod
    def linkExists(link: str) -> bool:
        """
        gibt true zurück, falls das Link in allen Playlists bereits existiert\n
        """

        #Suchen nach Link in Playlists
        for playlist in PlaylistService.allPlaylists:
            if playlist.link == link:
                return True
            
        #Ansonsten false returnen
        return False


    @staticmethod
    def updatePlaylist(id: int, title: str, description: str, tagStrings: list[str]):
        """
        updated die Daten einer Playlist
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)

        #Playlist Daten werden geupdatet
        playlist.title = title
        playlist.description = description
        try:
            PlaylistService.updateTags(id, tagStrings)
        except PlaylistServiceError as e:
            raise PlaylistServiceError(f"Could not add tags to playlist with id {id}")

        #TODO: kann später entfernt werden, wird von der Datenbank übernommen
        playlist.updatedAt = datetime.now()
        return
    
    
    @staticmethod
    def updateTags(id: int, tagTitles : list[str]):
        """
        updated die Tags einer Playlist
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """
        from app.services import tagService as tag

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)
        
        #Neue Liste für Tags erstellen und durchiterieren
        tags = []
        for tagTitle in tagTitles:
            
            #Tag erstellen, falls es noch nicht existiert
            try:
                tag.TagService.createTag(tagTitle)
            except tag.TagServiceError as e:
                print(e)
            
            #Tag auslesen
            try:
                _t = tag.TagService.findTag(tagTitle)
            
            #Falls nicht gefunden, Schleifeniteration skippen
            except tag.TagServiceError as e:
                print(e)
                continue

            #Gefundenen Tag der neuen Liste ergänzen
            tags.append(_t.id)

        #Alte Liste mit der neuen ersetzen
        playlist.tags = tags
        return
    

    @staticmethod
    def addTag(id: int, tagTitle: str):
        """
        adds a tag with tagTitle to playlist with id
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        - tag could not be found/created
        """
        from app.services import tagService as tag

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)

        #Tag erstellen, falls es noch nicht existiert
        try:
            tag.TagService.createTag(tagTitle)
        except tag.TagServiceError as e:
            print(e)
        
        #Tag auslesen
        try:
            _t = tag.TagService.findTag(tagTitle)
        
        #Falls nicht gefunden, PlaylistError ausgeben
        except tag.TagServiceError as e:
            raise PlaylistServiceError(f"Could not add tag {tagTitle} to playlist with id {id}")

        #Tag-ID der Liste in der Playlist ergänzen
        playlist.tags.append(_t.id)
        return


    @staticmethod
    def deletePlaylist(id: int):
        """
        löscht eine Playlist + alle Votes der Playlist\n
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """
        from app.services import vote

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)
        
        #Votes der Playlist werden gelöscht
        vote.VoteService.deleteAllPlaylistVotes(id)

        #Playlist wird gelöscht
        PlaylistService.allPlaylists.remove(playlist)
        return


    @staticmethod
    def removeTagFromAllPlaylists(tid: int):
        """
        löscht das Tag mit der tid aus allen Playlists\n
        """
        from app.services import tagService

        #Tag in allen Playlists suchen und löschen
        for playlist in PlaylistService.allPlaylists:
            try:
                containsTag = PlaylistService.containsTag(playlist.id, tid)
            except PlaylistServiceError as e:
                continue
            if (containsTag):
                playlist.tags.remove(tid)
        return
    

    @staticmethod
    def deleteAllUserPlaylists(uid: int):
        """
        löscht alle Playlist des Nutzers mit der uid\n
        """

        #Playlists des Users suchen und löschen
        for playlist in PlaylistService.allPlaylists:
            if (playlist.createdBy == uid):
                try:
                    PlaylistService.deletePlaylist(playlist.id)
                except PlaylistServiceError as e:
                    print(e)
        return
