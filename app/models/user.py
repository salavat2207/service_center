from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	email = Column(String, unique=True, index=True)
	hashed_password = Column(String)
	city_id = Column(Integer, ForeignKey("cities.id"))
	role = Column(String)  # admin или manager
	is_active = Column(Boolean, default=True)
	telegram_id = Column(String, nullable=True)

	# Отношения
	city = relationship("City", back_populates="users")