from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
	username: str
	email: EmailStr
	city_id: int
	role: str
	is_active: bool = True
	telegram_id: Optional[str] = None


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int

	class Config:
		orm_mode = True


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None
	role: Optional[str] = None
	city_id: Optional[int] = None