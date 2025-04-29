from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
	name: str
	description: str
	price: float
	image_url: Optional[str] = None
	is_available: bool = True
	city_id: Optional[int] = None


class ProductCreate(ProductBase):
	pass


class Product(ProductBase):
	id: int

	class Config:
		orm_mode = True