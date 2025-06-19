from typing import Optional
from pydantic import BaseModel, Field
from faker import Faker


fake = Faker()

class CreateUserRequest(BaseModel):
    """
    payload для POST /users
    Значения по умолчанию генерируются через faker.
    """
    name: str = Field(default_factory=fake.name)
    job: str  = Field(default_factory=fake.job)


class UpdateUserRequest(BaseModel):
    """
    payload для PUT /users/{id}
    Можно обновить и name, и job, или только одно поле.
    """
    name: Optional[str] = None
    job:  Optional[str] = None