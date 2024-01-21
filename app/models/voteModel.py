from datetime import datetime


class VoteModel:
    def __init__(self, id: int, uid: int, pid: int, tid: int, voteValue: int, createdAt: int, updatedAt: int):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.tid = tid
        #value=1 => upvote
        #value=-1 => downvote
        #value=0 => entfernen/neutral
        self.voteValue = voteValue or 0
        self.createdAt = createdAt or int(datetime.now().timestamp())
        self.updatedAt = updatedAt or int(datetime.now().timestamp())

    def __repr__(self) -> str:
        return f"""Vote {{
            id={self.id};
            uid={self.uid};
            pid={self.pid};
            tid={self.tid};
            voteValue={self.voteValue};
            createdAt={self.createdAt};
            updatedAt={self.updatedAt};
        }}"""