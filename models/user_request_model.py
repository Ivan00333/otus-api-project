from typing import Optional
from pydantic import BaseModel, Field
from faker import Faker


fake = Faker()

class CreateUserRequest(BaseModel):
    name: str = Field(default_factory=fake.name)
    job: str  = Field(default_factory=fake.job)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    job:  Optional[str] = None