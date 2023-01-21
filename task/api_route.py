from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from sql_app.models import Task
from sql_app.models import User
from sql_app.session import get_db
from task.utils import sync_with_trello
from task.utils import validate_fields
from users.api_route import get_current_user_from_token

router = APIRouter()


@router.post("/create-task")
async def create_task(
    type: str,
    title: str = None,
    description: str = None,
    category: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    limit_second=Depends(RateLimiter(times=1, seconds=1)),
    limit_min=Depends(RateLimiter(times=10, seconds=60)),
):
    errors = await validate_fields(type, title, description, category)
    if errors.keys():
        return JSONResponse(status_code=400, content=errors)
    task = Task(type=type)
    if title:
        task.title = title
    if description:
        task.description = description
    if category:
        task.category = category
    db.add(task)
    db.commit()
    db.refresh(task)
    await sync_with_trello(task=task, db=db)
    return task
