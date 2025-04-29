from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class RequestBase(BaseModel):
	name: str
	phone: str
	email: Optional[EmailStr] = None
	city_id: int
	message: str
	service_id: Optional[int] = None
	product_id: Optional[int] = None


class RequestCreate(RequestBase):
	pass


class RequestUpdate(BaseModel):
	status: str


class Request(RequestBase):
	id: int
	status: str
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True