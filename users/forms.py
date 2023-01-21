from typing import List
from typing import Optional

from fastapi import Request


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.last_name = form.get("last_name")
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.name:
            self.errors.append("Name is required")
        if not self.last_name:
            self.errors.append("Last name is required")
        if not self.email:
            self.errors.append("Email is required")
        if self.email and not (self.email.__contains__("@")):
            self.errors.append("Enter a valid email")
        if not self.password or not len(self.password) >= 8:
            self.errors.append("Password must have more than 8 chars")
        if self.password and not any(filter(str.islower, self.password)):
            self.errors.append("Password must contain lowercase chars")
        if self.password and not any(filter(str.isupper, self.password)):
            self.errors.append("Password must contain uppercase chars")
        if self.password and not any(filter(str.isnumeric, self.password)):
            self.errors.append("Password must contain numeric chars")
        if not self.errors:
            return True
        return False


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "email"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
