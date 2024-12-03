from sqlalchemy import Column, Integer, String
from . import  Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column("id", Integer, primary_key=True)
    topic = Column("topic", String)
    company = Column("company", String)
    body = Column("name", String)
    country = Column("created_by", String)
    state = Column("going", String)
    zip_code = Column("maybe", String)
    sender = Column("sender", String)
    receiver = Column("receiver", String)
    serialized = Column("serialized", String)

    def __init__(self, body="", topic="", company="", country="", state="", zip_code="", sender="", receiver="", serialized=""):
        self.body = body
        self.country = country
        self.state = state
        self.zip_code = zip_code
        self.sender = sender
        self.receiver = receiver
        self.topic = topic
        self.serialized = serialized
