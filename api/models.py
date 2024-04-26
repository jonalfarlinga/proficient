from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    username: str
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    name: str


class UserOutWithPassword(UserIn):
    password: str


class DatabaseError(BaseModel):
    failure: str
    detail: str
