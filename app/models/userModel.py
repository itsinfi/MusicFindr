from datetime import datetime


class UserModel:
    def __init__(self, id: int, password: str, username: str, createdAt: datetime, updatedAt: datetime):
        self.id = id
        self.password = password or ""
        self.username = username or ""
        self.createdAt = int(createdAt.timestamp()) or int(datetime.now().timestamp())
        self.updatedAt = int(updatedAt.timestamp()) or int(datetime.now().timestamp())

    def __repr__(self) -> str:
        return f"""User {{
            id={self.id};
            username={self.username};
            password={self.password};
            createdAt={self.createdAt};
            updatedAt={self.updatedAt};
        }}"""