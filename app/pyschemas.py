from pydantic import BaseModel


class Usercreate(BaseModel):
    username: str
    email: str
    password: str


class Userlogin(BaseModel):
    email: str
    password: str
