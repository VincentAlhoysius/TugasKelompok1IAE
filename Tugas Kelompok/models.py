from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str


class Item(BaseModel):
    id: int
    name: str
    price: int


class ProfileUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]