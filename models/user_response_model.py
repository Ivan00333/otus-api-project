from typing import List
from pydantic import BaseModel, HttpUrl


class UserData(BaseModel):
    id:         int
    email:      str
    first_name: str
    last_name:  str
    avatar:     HttpUrl


class UsersListResponse(BaseModel):
    page:        int
    per_page:    int
    total:       int
    total_pages: int
    data:        List[UserData]


class SingleUserResponse(BaseModel):
    data:    UserData
    support: dict  # можно расписать в отдельную модель, если нужно


class CreateUserResponse(BaseModel):
    name:      str
    job:       str
    id:        str
    createdAt: str


class UpdateUserResponse(BaseModel):
    name:      str
    job:       str
    updatedAt: str

class RegisterResponse(BaseModel):
    id: int
    token: str
