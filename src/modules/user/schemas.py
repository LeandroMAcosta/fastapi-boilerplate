from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserSchema(UserBase):
    id: int
    name: str
    last_name: str

    model_config = {"from_attributes": True}
