from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sql_app.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Task(Base):
    __tablename__ = "tasks"

    ISSUE = "issue"
    TASK = "task"
    BUG = "bug"

    TYPES = [(ISSUE, "Issue"), (TASK, "Task"), (BUG, "Bug")]

    CATEGORIES = [
        ("maintenance", "Maintenance"),
        ("research", "Research"),
        ("test", "Test"),
    ]

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    title = Column(String)
    description = Column(String)
    category = Column(String)


class Label(Base):
    id = Column(Integer, primary_key=True, index=True)
    trello_id = Column(String, index=True)
    name = Column(String)
