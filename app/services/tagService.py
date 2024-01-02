from datetime import datetime
from app.models import tagModel as t

class TagService:
    allTags = []

    #für testen only!!!
    @staticmethod
    def _createTag(id: int, title: str, createdAt: datetime):
        if (TagService.tagExists(id)):
            print(f"tag already exists")
            return

        tag = t.TagModel(id, title, createdAt)
        TagService.allTags.append(tag)
        print(TagService.allTags)    
        return
    
    @staticmethod
    def createTag(title: str):
        if (TagService.titleExists(title)):
            print(f"Title already exists!")
            return
        

        #TODO: bitte später entfernen, das ist erstmal rein zum testen!!!!
        id = 1
        while (TagService.tagExists(id)):
            id += 1

        tag = t.TagModel(id, title, datetime.now())
        TagService.allTags.append(tag)
        print(TagService.allTags)
        return
    
    @staticmethod
    def readTag(id: int) -> t.TagModel:
        for tag in TagService.allTags:
            if tag.id == id:
                print(tag)
                return tag
        else:
            print(f"tag with id {id} not found")
            return

    @staticmethod
    def findTag(title: str) -> t.TagModel:
        for tag in TagService.allTags:
            if tag.title == title:
                print(tag)
                return tag
        else:
            print(f"tag with title {title} not found")

    @staticmethod
    def tagExists(id: int) -> bool:
        for tag in TagService.allTags:
            if tag.id == id:
                print(tag)
                return True
        else:
            print(f"tag with id {id} not found")
            return False

    @staticmethod
    def titleExists(title: str) -> bool:
        for tag in TagService.allTags:
            if tag.title == title:
                print(tag)
                return True
        else:
            print(f"tag with title {title} not found")
            return False
    
    @staticmethod
    def updateTag(id: int, title: str):
        tag = TagService.readTag(id)
        if tag is None:
            print("Tag existiert nicht!")
            return
        
        tag.title = title
        print(f"Deleted tag with id {id}")
        print(TagService.allTags)
        return
    
    @staticmethod
    def deleteTag(id: int):
        from app.services import playlist
        from app.services import vote
        tag = TagService.readTag(id)
        if tag is None:
            print("Tag existiert nicht!")
            return

        vote.VoteService.deleteAllTagVotes(id) #alle verbundenen Votes löschen
        playlist.PlaylistService.removeTagFromAllPlaylists(id) #aus allen verbundenen Playlists Referenzierung entfernen
        TagService.allTags.remove(tag)
        print(TagService.allTags)
        return