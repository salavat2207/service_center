from pydantic import BaseModel
from typing import List, Optional


class CityBase(BaseModel):
	name: str
	active: bool = True


class CityCreate(CityBase):
	pass


class City(CityBase):
	id: int

	class Config:
		orm_mode = True