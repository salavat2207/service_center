from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Product(Base):
	__tablename__ = "products"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	description = Column(String)
	price = Column(Float)
	image_url = Column(String, nullable=True)
	is_available = Column(Boolean, default=True)
	city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)

	# Отношения
	city = relationship("City", back_populates="products")
	requests = relationship("Request", back_populates="product")