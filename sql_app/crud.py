from sqlalchemy.orm import Session

from core.hashing import Hasher
from sql_app import models
from sql_app import schemas


# --------- USER ----------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_new_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --------- TASK ----------
def list_tasks(db: Session):
    tasks = db.query(models.Task).all()
    return tasks


def search_task(query: str, db: Session):
    tasks = db.query(models.Task).filter(models.Task.title.contains(query))
    return tasks


# --------- LABEL ----------
def get_label(db: Session, label: str):
    return db.query(models.Label).filter(models.Label.name == label).first()
