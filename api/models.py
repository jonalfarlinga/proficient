from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    username: str
    name: str
    password: str


class UserUpdate(UserIn):
    new_email: str | None = None
    new_password: str | None = None


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    name: str


class UserOutWithPassword(UserOut):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class DatabaseError(BaseModel):
    failure: str
    detail: str

    def __str__(self):
        return f"Database Error: {self.failure}\n{self.detail}"

    def __repr__(self):
        return self.__str__()
