from datetime import datetime
from random import shuffle
import re
import requests
from app.models import playlistModel as p

class PlaylistServiceError(Exception):
    """
    Custom Error Klasse für Methoden des PlaylistService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class PlaylistSearchServiceError(Exception):
    """
    Custom Error Klasse für Methoden des PlaylistService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, query): 
        self.message = f"Keine Playlist gefunden für die Suchanfrage: {query}"
        super().__init__(self.message)

class PlaylistQueryServiceError(Exception):
    """
    Custom Error Klasse für Methoden des PlaylistService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message): 
        self.message = f"Keine Suchanfrage eingegeben"
        super().__init__(self.message)

class PlaylistService:
    allPlaylists = []


    #only for testing
    @staticmethod
    def _createPlaylist(id: int, link: str, title: str, description: str, tagStrings: list[str], createdBy: int, createdAt: int, updatedAt: int):
        """
        erstellt eine Playlist (bitte nur für Testzwecke nutzen)\n
        throws PlaylistServiceException if:
        - playlist with id already exists
        - link/title/description/tag requirements are not fulfilled (individual error message)
        """
        from app.services import tagService as tag
        
        #Prüfung, ob Playlist-ID bereits existiert
        if (PlaylistService.playlistExists(id)):
            raise PlaylistServiceError(f"Playlist with id {id} already exists.")
        
        platform = PlaylistService.getLinkPlatform(link)

        #Playlist erstellen
        playlist = p.PlaylistModel(id, link, title, description, createdBy, createdAt, updatedAt, platform)

        #Playlist zur Playlist list hinzufügen
        PlaylistService.allPlaylists.append(playlist)

        #Tags der Playlist hinzufügen
        try:
            PlaylistService.updateTags(id, tagStrings)
        except PlaylistServiceError as e:
            raise PlaylistServiceError(f"Etwas ist beim Hinzufügen der Tags schief gelaufen.")
        return
    

    @staticmethod
    def createPlaylist(link: str, title: str, description: str, tagStrings: list[str], createdBy: int):
        """
        erstellt eine Playlist\n
        throws UserException if:
        - link/title/description/tag requirements are not fulfilled (individual error message)
        """
        from app.services import tagService as tag
        #if (not PlaylistService.linkExists(link)):

        #Link checken
        PlaylistService.validateLink(link)

        #Title checken
        PlaylistService.validateTitle(title)

        #Description checken
        PlaylistService.validateDescription(description)

        #Tags checken
        try:
            for tagString in tagStrings:
                tag.TagService.validateTitle(tagString)
        except tag.TagServiceError as e:
            raise PlaylistServiceError(e.message)

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (PlaylistService.playlistExists(id)):
            id += 1

        platform = PlaylistService.getLinkPlatform(link)

        #Playlist erstellen
        playlist = p.PlaylistModel(id, link, title, description, createdBy, int(datetime.now().timestamp()), int(datetime.now().timestamp()), platform)

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
    def validateDescription(description: str) -> bool:
        """
        checks a description for the following criteria\n
        (throws an PlaylistServiceException if not fulfilled):
        - maximum of 256 characters long
        - only contains letters (a-z), numbers + certain symbols and emojis ;)
        """

        #Checken, ob die Beschreibung leer ist
        if not description:
            return True

        #Checken, ob die Beschreibung zu lang ist
        if not len(description) < 256:
            raise PlaylistServiceError("The description is longer than 256 characters.")
        
        #Characters checken
        regex = r"^[A-Za-z0-9ÄÖÜäöüß -_.:'\",&!\*()\[\]+#\?\$\€\n\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+$"
        if not (re.match(regex, description)):
            raise PlaylistServiceError("The description contains invalid characters. Allowed are only letters, numbers, some commonly used symbols and emojis.")
        
        #Anforderungen erfüllt
        return True


    @staticmethod
    def validateTitle(title: str) -> bool:
        """
        checks a title for the following criteria\n
        (throws an PlaylistServiceException if not fulfilled):
        - at least 1 character long
        - maximum of 32 characters long
        - only contains letters (a-z), numbers + certain symbols and emojis ;)
        """

        #Checken, ob der Titel zu kurz ist
        if not len(title) > 0:
            raise PlaylistServiceError("The title is empty. The field is required.")

        #Checken, ob der Titel zu lang ist
        if not len(title) < 32:
            raise PlaylistServiceError("The title is longer than 32 characters.")
        
        #Characters checken
        regex = r"^[A-Za-z0-9äöüß -_.:'\",&!\*()\[\]+#\?\$\€\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+$"
        if not (re.match(regex, title)):
            raise PlaylistServiceError("The title contains invalid characters. Allowed are only letters, numbers, some commonly used symbols and emojis.")
        
        #Anforderungen erfüllt
        return True


    @staticmethod
    def validateLink(link: str) -> bool:
        """
        checks a link for the following criteria\n
        (throws an PlaylistServiceException if not fulfilled):
        - link is a spotify, youtube, yt music or souncloud link for a playlist
        - link is no longer than 256 characters
        - the link also needs to return a 200 response
        """

        #Checken, ob der Link zu lang ist
        if not len(link) < 256:
            raise PlaylistServiceError("The link is longer than 256 characters.")

        #Check, ob der Link 200 returned
        try:
            response = requests.get(link)
            if (response.status_code != 200):
                raise PlaylistServiceError("The link cannot be opened. Make sure the link is valid.")
        except requests.exceptions.RequestException:
            raise PlaylistServiceError("The link cannot be opened. Make sure the link is valid.")

        #Spotify
        spotify = r'https?://(?:www\.)?open\.spotify\.com/playlist/[a-z0-9&?_=]*'
        if (re.match(spotify, link)):
            return True

        #YouTube
        yt = r'https?://(?:www\.)?youtube\.com/playlist\?list=[a-z0-9&?_=]*'
        if (re.match(yt, link)):
            return True

        #YT Music
        ytMusic = r'https?://(?:www\.)?music\.youtube\.com/playlist\?list=[a-z0-9&?_=]*'
        if (re.match(ytMusic, link)):
            return True

        #SoundCloud
        sc = r'https?://(?:www\.)?soundcloud\.com/[a-z0-9_-]*/sets/[a-z0-9&?_=]*|https?://(?:www\.)?on\.soundcloud\.com/[a-z0-9&?_=]*'
        if (re.match(sc, link)):
            return True

        #Otherwise
        raise PlaylistServiceError("Currently, we only support Spotify, YouTube, YouTube Music and SoundCloud links. Make sure it leads to a playlist and that it is not a 3rd party link redirection.")


    @staticmethod
    def readPlaylist(id: int) -> p.PlaylistModel:
        """
        gibt eine Playlist der ID zurück, falls diese existiert\n
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """

        #Suchen nach Playlist mit der ID
        for playlist in PlaylistService.allPlaylists:
            # print("\nid:")
            # print(playlist.id)
            # print("\nname:")
            # print(playlist.title)
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
        - link/title/description/tag requirements are not fulfilled (individual error message)
        """
        from app.services import tagService as tag

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)

        #Title checken
        PlaylistService.validateTitle(title)

        #Description checken
        PlaylistService.validateDescription(description)

        #Playlist Daten werden geupdatet
        playlist.title = title
        playlist.description = description
        try:
            PlaylistService.updateTags(id, tagStrings)
        except PlaylistServiceError as e:
            raise PlaylistServiceError(f"Could not add tags to playlist with id {id}")

        #TODO: kann später entfernt werden, wird von der Datenbank übernommen
        playlist.updatedAt = int(datetime.now().timestamp())
        return
    
    
    @staticmethod
    def updateTags(id: int, tagTitles : list[str]):
        """
        updated die Tags einer Playlist
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        - tag requirements are not fulfilled (individual error message)
        """
        from app.services import tagService as tag

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)

        #Tags checken
        try:
            for tagString in tagTitles:
                tag.TagService.validateTitle(tagString)
        except tag.TagServiceError as e:
            raise PlaylistServiceError(e.message)
        
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
        from app.services import tagService as ts

        tag = None

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)

        try:
            tag = ts.TagService.findTag(tagTitle)
        except ts.TagServiceError as e:
            print(e)

        print(type(tag))
        print(tag)
        
        if tag is None:
            try:
                ts.TagService.createTag(tagTitle)
                tag = ts.TagService.findTag(tagTitle)
            except ts.TagServiceError as e:
                raise PlaylistServiceError(e.message)
        
        if tag.id in playlist.tags:
            raise PlaylistServiceError(f"Tag {tagTitle} already exists in Playlist with id {id}")

        #Tag-ID der Liste in der Playlist ergänzen
        try:
            playlist.tags.append(tag.id)
        except Exception as e:
            raise PlaylistServiceError(f"Tag {tagTitle} could not be added to Playlist with id {playlist.id}")
        return


    @staticmethod
    def deletePlaylist(id: int):
        """
        löscht eine Playlist + alle Votes der Playlist\n
        throws PlaylistServiceError if:
        - playlist with specified id does not exist
        """
        from app.services import vote
        from app.services import sqlService as sql

        #Playlist wird ausgelesen (+ Prüfung, ob Playlist existiert)
        playlist = PlaylistService.readPlaylist(id)
        
        #Votes der Playlist werden gelöscht
        vote.VoteService.deleteAllPlaylistVotes(id)

        #Playlist wird gelöscht
        PlaylistService.allPlaylists.remove(playlist)

        print(PlaylistService.allPlaylists)

        #Verbindungen zu Tags in der DB werden gelöscht
        sql.sqlService.deleteAllContainingID("TagPlaylist_Relationship", "pid", id)

        #Playlist wird aus der DB gelöscht
        sql.sqlService.delete("Playlist", id)
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

        ids = []
        #Playlists des Users suchen und löschen
        for playlist in PlaylistService.allPlaylists:
            if (playlist.createdBy == uid):
                ids.append(playlist.id)
                
        for id in ids:
            try:
                PlaylistService.deletePlaylist(id)
            except PlaylistServiceError as e:
                print(e)
        return
    
    @staticmethod
    def searchPlaylist(query: str):
        """
        gibt eine Liste mit Playlists zurück, falls diese existiert\n
        """
        from app.services import tagService
        # Suchen nach Playlist mit den Tags
        Research = []
        for playlist in PlaylistService.allPlaylists:
            for tagId in playlist.tags :
                try :
                    tag = tagService.TagService.readTag(tagId)
                except tagService.TagServiceError as e: 
                    print(e)
                    continue
                    

                if query.lower() in tag.title.lower() and playlist not in Research:
                    Research.append(playlist)
        return Research
    
    @staticmethod
    def getShuffledPlaylist():
        """
        Gibt eine zufällig sortierte Liste aller Playlists zurück.
        """
        shuffled_playlist = PlaylistService.allPlaylists.copy()
        shuffle(shuffled_playlist)
        return shuffled_playlist

    @staticmethod
    def tagsToTagList(tags: str) -> list[str]:
        tagList = tags.split(',')
        return [tag.strip() for tag in tagList]
    
    @staticmethod
    def getLinkPlatform(link: str) -> str:
        if "open.spotify." in link:
            return "spotify"
        if "music.youtube." in link:
            return "youtubemusic"
        if "youtube." in link:
            return "youtube"
        if "soundcloud." in link:
            return "soundcloud"
        return ""
    
    # @staticmethod
    # def getsortedplaylist():
    #     """
    #     gibt eine nach dem erstellungsdatum sortierte liste aller playlists zurück.
    #     """
    #     sort = playlistservice.allplaylists.copy()
        
    #     # sortiere die playlists nach dem erstellungsdatum
    #     sorted_playlist = sorted(sort, key= sort.createdat)
        
    #     return sorted_playlist

    @staticmethod 
    def getUserPlaylists(user_id):
        user_playlists = []

        all_playlists = PlaylistService.allPlaylists.copy()

        for playlist in all_playlists:
            if playlist.createdBy == user_id:
                user_playlists.append(playlist)

        return user_playlists
    
    