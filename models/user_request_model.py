from multiprocessing.connection import default_family
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from faker import Faker


fake = Faker()

class CreateUserRequest(BaseModel):
    name: str = Field(default_factory=fake.name)
    job: str  = Field(default_factory=fake.job)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    job:  Optional[str] = None

class RegisterRequest(BaseModel):
    email: EmailStr = Field(default="eve.holt@reqres.in")
    password: str = Field(default="pistol")

class RegisterUnknownUserRequest(BaseModel):
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=lambda: fake.password(6))