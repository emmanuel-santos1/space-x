from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import responses
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from sql_app.crud import create_new_user
from sql_app.schemas import UserCreate
from sql_app.session import get_db
from users.api_route import login_for_access_token
from users.forms import LoginForm
from users.forms import UserCreateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
async def register_post(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            name=form.name,
            last_name=form.last_name,
            email=form.email,
            password=form.password,
        )
        try:
            user = create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login_post(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response
