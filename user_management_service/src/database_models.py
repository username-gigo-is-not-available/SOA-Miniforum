from pydantic import BaseModel, Field, validator


class User(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    hashed_password: str = Field(...)

    @validator("email")
    def validate_email(cls, value):
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "username": "John Doe",
                "email": "john.doe@example.com",
                "hashed_password": "cfa30f71e3d0d16e1390c908bfe3c5680be6612b6e0eef51836bd4556c3e2f16"
            }
        }
