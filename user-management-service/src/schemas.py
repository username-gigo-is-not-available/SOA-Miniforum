from pydantic import BaseModel, Field, EmailStr, validator


class UserBase(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


    @validator("email")
    def validate_email(cls, value):
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserLogin(UserBase):
    pass
