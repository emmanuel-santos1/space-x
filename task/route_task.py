from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from sql_app.crud import list_tasks
from sql_app.crud import search_task
from sql_app.session import get_db
from users.api_route import get_current_user_from_token


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    tasks = list_tasks(db=db)
    authorization: str = request.cookies.get("access_token", None)
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        user = None
        tasks = []
    else:
        try:
            user = get_current_user_from_token(token, db)
        except HTTPException:
            user = None
            tasks = []
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {"request": request, "tasks": tasks, "user": user, "msg": msg},
    )


@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    tasks = search_task(query, db=db)
    authorization: str = request.cookies.get("access_token", None)
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        user = None
        tasks = []
    else:
        try:
            user = get_current_user_from_token(token, db)
        except HTTPException:
            user = None
            tasks = []
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {"request": request, "user": user, "tasks": tasks},
    )
