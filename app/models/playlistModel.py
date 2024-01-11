from datetime import datetime


class PlaylistModel:
    def __init__(self, id: int, link: str, title: str, description: str, createdBy: int, createdAt: datetime, updatedAt: datetime):
        self.id = id
        self.link = link or ""
        self.title = title or ""
        self.description = description or ""
        self.tags : list[int] = []
        self.createdBy = createdBy
        self.createdAt = createdAt or datetime.now()
        self.updatedAt = updatedAt or datetime.now()
    
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
