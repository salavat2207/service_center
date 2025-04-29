from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
import datetime

from ..database import Base


class Request(Base):
	__tablename__ = "requests"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)  # Имя клиента
	phone = Column(String)
	email = Column(String, nullable=True)
	city_id = Column(Integer, ForeignKey("cities.id"))
	message = Column(String)
	service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
	status = Column(String, default="new")  # new, processing, completed, cancelled
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	# Отношения
	city = relationship("City", back_populates="requests")
	service = relationship("Service", back_populates="requests")
	product = relationship("Product", back_populates="requests")