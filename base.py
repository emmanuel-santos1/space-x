from fastapi import APIRouter

from sql_app import models
from sql_app.session import engine
from task import api_route as api_route_task
from task import route_task
from users import api_route as api_route_user
from users import route_users

models.Base.metadata.create_all(bind=engine)

api_router = APIRouter()
api_router.include_router(route_task.router, prefix="", tags=["task"])
api_router.include_router(route_users.router, prefix="", tags=["users"])
api_router.include_router(api_route_task.router, prefix="", tags=["api-tasks"])
api_router.include_router(api_route_user.router, prefix="", tags=["api-users"])
