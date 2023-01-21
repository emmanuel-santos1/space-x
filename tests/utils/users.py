from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from sql_app.crud import create_new_user
from sql_app.crud import get_user_by_email
from sql_app.schemas import UserCreate


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    name = "fake-name"
    last_name = "fake-last_name"
    user = get_user_by_email(email=email, db=db)
    if not user:
        user_in_create = UserCreate(
            name=name, last_name=last_name, email=email, password=password
        )
        user = create_new_user(user=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)
