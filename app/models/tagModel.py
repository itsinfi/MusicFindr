from datetime import datetime


class TagModel:
    def __init__(self, id: int, title: str, createdAt: int):
        self.id = id
        self.title = title or ""
        self.createdAt = createdAt or int(datetime.now().timestamp())
    
    def __repr__(self) -> str:
        return f"""Tag {{
            id={self.id};
            title={self.title}; 
            createdAt={self.createdAt};
        }}"""