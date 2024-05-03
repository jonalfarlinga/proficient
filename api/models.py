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


class Token(BaseModel):
    access_token: str
    token_type: str


class DatabaseError(BaseModel):
    failure: str
    detail: str

    def __str__(self):
        return f"Database Error: {self.failure}\n{self.detail}"

    def __repr__(self):
        return self.__str__()
