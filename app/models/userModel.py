from datetime import datetime


class UserModel:
    def __init__(self, id: int, password: str, username: str, createdAt: int, updatedAt: int):
        self.id = id
        self.password = password or ""
        self.username = username or ""
        self.createdAt = createdAt or int(datetime.now().timestamp())
        self.updatedAt = updatedAt or int(datetime.now().timestamp())

    def __repr__(self) -> str:
        return f"""User {{
            id={self.id};
            username={self.username};
            password={self.password};
            createdAt={self.createdAt};
            updatedAt={self.updatedAt};
        }}"""