from datetime import datetime


class PlaylistModel:
    def __init__(self, id: int, link: str, title: str, description: str, createdBy: int, createdAt: int, updatedAt: int):
        self.id = id
        self.link = link or ""
        self.title = title or ""
        self.description = description or ""
        self.tags : list[int] = []
        self.createdBy = createdBy
        self.createdAt = createdAt or int(datetime.now().timestamp())
        self.updatedAt = updatedAt or int(datetime.now().timestamp())
    
    def __repr__(self) -> str:
        return f"""Playlist {{
            id={self.id};
            link={self.link};
            title={self.title};
            description={self.description};
            tags={self.tags}
            createdBy={self.createdBy};
            createdAt={self.createdAt};
            updatedAt={self.updatedAt};
        }}"""