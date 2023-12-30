from datetime import datetime


class UserModel:
    def __init__(self, id: int, password: str, username: str, createdAt: datetime, updatedAt: datetime):
        self.id = id
        self.password = password or ""
        self.username = username or ""
        self.createdAt = createdAt or datetime.now()
        self.updatedAt = updatedAt or datetime.now()

    def __repr__(self) -> str:
        return f"""User {{
            id={self.id};
            username={self.username};
            password={self.password};
            createdAt={self.createdAt};
            updatedAt={self.updatedAt};
        }}"""