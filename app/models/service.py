from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Service(Base):
	__tablename__ = "services"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	description = Column(String)
	price = Column(Float)
	estimated_time = Column(String)
	is_available = Column(Boolean, default=True)
	city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)

	# Отношения
	city = relationship("City", back_populates="services")
	requests = relationship("Request", back_populates="service")