from pydantic import BaseModel
from typing import Optional


class ServiceBase(BaseModel):
	name: str
	description: str
	price: float
	estimated_time: str
	is_available: bool = True
	city_id: Optional[int] = None


class ServiceCreate(ServiceBase):
	pass


class Service(ServiceBase):
	id: int

	class Config:
		orm_mode = True