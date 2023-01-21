import json

import requests
from sqlalchemy.orm import Session

from core.config import settings
from sql_app.crud import get_label
from sql_app.models import Label
from sql_app.models import Task

url = "https://api.trello.com/1"

headers = {"Accept": "application/json"}

default_query = {
    "idList": settings.TRELLO_TO_DO_LIST_ID,
    "key": settings.TRELLO_API_KEY,
    "token": settings.TRELLO_API_TOKEN,
}


async def validate_fields(type: str, title: str, description: str, category: str):
    errors = {}
    if type not in [x[0] for x in Task.TYPES]:
        errors["type"] = f"'{type}' is an invalid type for tasks."
    if not category and type == Task.TASK:
        errors["category"] = f"The type '{type}' required caregory field."
    if category:
        if type != Task.TASK:
            errors["category"] = f"The type '{type}' don't support caregory field."
        else:
            if category not in [x[0] for x in Task.CATEGORIES]:
                errors["category"] = f"'{category}' is an invalid category."
    if title and type == Task.BUG:
        errors["title"] = f"The type '{type}' don't support title field."
    if not title and type != Task.BUG:
        errors["title"] = f"The type '{type}' required title field."
    if description and type == Task.TASK:
        errors["description"] = f"The type '{type}' don't support description field."
    if not description and type != Task.TASK:
        errors["description"] = f"The type '{type}' required description field."
    return errors


async def get_id_label(label: str, db: Session):
    label_id = None
    label_obj = get_label(db=db, label=label)
    if not label_obj:
        label_id = await create_label(label=label, db=db)
    else:
        label_id = label_obj.trello_id
    return label_id


async def create_label(label: str, db: Session):
    label_obj = Label(name=label)
    query = default_query.copy()
    query["idBoard"] = settings.TRELLO_BOARD_ID
    query["name"] = label
    response = requests.request("POST", f"{url}/labels", headers=headers, params=query)
    response_data = json.loads(response.text)
    label_id = response_data["id"]
    label_obj.trello_id = label_id
    db.add(label_obj)
    db.commit()
    db.refresh(label_obj)
    return label_id


async def sync_with_trello(task: Task, db: Session):
    query = default_query.copy()
    if task.title:
        query["name"] = str(task.title)
    if task.description:
        query["desc"] = task.description
    if task.category:
        query["idLabels"] = await get_id_label(label=task.category, db=db)
    if task.type == Task.BUG:
        query["idLabels"] = await get_id_label(label="bug", db=db)
    requests.request("POST", f"{url}/cards", headers=headers, params=query)
