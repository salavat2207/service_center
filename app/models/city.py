from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class City(Base):
	__tablename__ = "cities"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)
	active = Column(Boolean, default=True)

	# Отношения
	users = relationship("User", back_populates="city")
	products = relationship("Product", back_populates="city")
	services = relationship("Service", back_populates="city")
	requests = relationship("Request", back_populates="city")