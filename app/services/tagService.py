from datetime import datetime
from random import sample
import re
from app.models import tagModel as t

class TagServiceError(Exception):
    """
    Custom Error Klasse für Methoden des TagService\n
    Bitte try except bei entsprechend gekennzeichneten Methoden verwenden!
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class TagService:
    allTags = []

    
    #only for testing
    @staticmethod
    def _createTag(id: int, title: str, createdAt: datetime):
        """
        erstellt einen Tag (bitte nur für Testzwecke nutzen)\n
        throws TagServiceException if:
        - tag with id already exists
        - title requirements are not fulfilled (individual error message)
        """

        #Prüfung, ob Tag ID bereits existiert
        if (TagService.tagExists(id)):
            raise TagServiceError(f"Tag with id {id} already exists.")
        
        #Prüfung, ob der Title bereits existiert
        if (TagService.titleExists(title)):
            raise TagServiceError(f"Tag with title {title} already exists.")
        
        #Title checken
        TagService.validateTitle(title)

        #Tag erstellen
        tag = t.TagModel(id, title, createdAt)

        #Tag zu Taglist hinzufügen
        TagService.allTags.append(tag)   
        return
    

    @staticmethod
    def createTag(title: str):
        """
        erstellt einen Tag\n
        throws TagServiceException if:
        - tag with title already exists
        - title requirements are not fulfilled (individual error message)
        """

        #Prüfung, ob der Title bereits existiert
        if (TagService.titleExists(title)):
            raise TagServiceError(f"Tag with title {title} already exists.")
        
        #Title checken
        TagService.validateTitle(title)

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (TagService.tagExists(id)):
            id += 1

        #Tag erstellen
        tag = t.TagModel(id, title, datetime.now())

        #Tag zur Taglist hinzufügen
        TagService.allTags.append(tag)
        return
    

    @staticmethod
    def validateTitle(title: str):
        """
        checks a title for the following criteria\n
        (throws an TagServiceException if not fulfilled):
        - at least 1 character long
        - maximum of 32 characters long
        - only contains letters (a-z), numbers and certain symbols
        """

        #Checken, ob der Titel zu kurz ist
        if not len(title) > 0:
            raise TagServiceError("The title is empty. The field is required.")

        #Checken, ob der Titel zu lang ist
        if not len(title) < 32:
            raise TagServiceError("The title is longer than 32 characters.")
        
        #Characters checken
        regex = r"^[A-Za-z0-9äöüß -_.,&()+#]+$"
        if not (re.match(regex, title)):
            raise TagServiceError("The title contains invalid characters. Allowed are only letters, numbers and some commonly used symbols.")
        
        #Anforderungen erfüllt
        return True
    

    @staticmethod
    def readTag(id: int) -> t.TagModel:
        """
        gibt einen Tag mit der ID zurück, falls dieser existiert\n
        throws TagServiceError if:
        - tag with specified id does not exist
        """

        #Suchen nach Tag mit der ID
        for tag in TagService.allTags:
            if tag.id == id:
                return tag
        
        #TagServiceError, falls nicht gefunden
        raise TagServiceError(f"Tag with id {id} could not be found or does not exist.")


    @staticmethod
    def findTag(title: str) -> t.TagModel:
        """
        gibt einen Tag mit dem Title zurück, falls dieser existiert\n
        throws TagServiceError if:
        - tag with specified id does not exist
        """

        #Suchen nach Tag mit dem Title
        for tag in TagService.allTags:
            if tag.title == title:
                return tag
        
        #TagServiceError, falls nicht gefunden
        raise TagServiceError(f"Tag with title {title} could not be found or does not exist.")


    @staticmethod
    def tagExists(id: int) -> bool:
        """
        prüft, ob ein Tag unter der ID bereits existiert
        """

        #Suchen nach Tag mit der ID
        for tag in TagService.allTags:
            if tag.id == id:
                return True
        
        #TagServiceError, falls nicht gefunden    
        return False


    @staticmethod
    def titleExists(title: str) -> bool:
        """
        prüft, ob ein Tag unter dem Titel bereits existiert
        """

        #Suchen nach Tag mit dem Title
        for tag in TagService.allTags:
            if tag.title == title:
                return True
        
        #TagServiceError, falls nicht gefunden
        return False

    
    ##########DO WE NEED THIS?
    @staticmethod
    def updateTag(id: int, title: str):
        """
        updated die Daten eines Tags\n
        throws TagServiceError if:
        - tag with specified id does not exist
        - title requirements are not fulfilled (individual error message)
        """

        #Tag wird ausgelesen (+ Prüfung, ob Tag existiert)
        tag = TagService.readTag(id)

        #Title checken
        TagService.validateTitle(title)
        
        #Tag wird geupdated
        tag.title = title
        return


    #########DO WE NEED THIS?????
    @staticmethod
    def deleteTag(id: int):
        """
        löscht einen Tag + alle Playlistseinträge des Tags und Votes zugehörig zum Tag\n
        throws TagServiceError if:
        - tag with specified id does not exist
        """
        from app.services import playlist
        from app.services import vote

        #Tag wird ausgelesen (+ Prüfung, ob Tag existiert)
        tag = TagService.readTag(id)

        #Alle Votes zugehörig zum Tag löschen
        vote.VoteService.deleteAllTagVotes(id)

        #Tag von allen Playlists mit dem Tag löschen
        playlist.PlaylistService.removeTagFromAllPlaylists(id)

        #Tag selbst löschen
        TagService.allTags.remove(tag)
        return
    
    @staticmethod
    def getThreeRandomTags():
        """
        Gibt eine Liste mit drei zufälligen Tags zurück.
        """
        return sample(TagService.allTags, min(3, len(TagService.allTags)))
