from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..utils.security import get_admin_user

router = APIRouter()

router.get("/cities", response_model=List[schemas.City])


def get_cities(db: Session = Depends(get_db), active: bool = True):
	"""
	Получить список городов
	"""
	if active:
		cities = db.query(models.City).filter(models.City.active == True).all()
	else:
		cities = db.query(models.City).all()
	return cities


@router.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
	"""
	Получить информацию о городе по ID
	"""
	city = db.query(models.City).filter(models.City.id == city_id).first()
	if city is None:
		raise HTTPException(status_code=404, detail="City not found")
	return city


@router.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db),
				current_user: models.User = Depends(get_admin_user)):
	"""
	Создать новый город (только для админов)
	"""
	db_city = db.query(models.City).filter(models.City.name == city.name).first()
	if db_city:
		raise HTTPException(status_code=400, detail="City already exists")

	db_city = models.City(**city.dict())
	db.add(db_city)
	db.commit()
	db.refresh(db_city)
	return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db),
				current_user: models.User = Depends(get_admin_user)):
	"""
	Обновить информацию о городе (только для админов)
	"""
	db_city = db.query(models.City).filter(models.City.id == city_id).first()
	if db_city is None:
		raise HTTPException(status_code=404, detail="Город не найден")

	for key, value in city.dict().items():
		setattr(db_city, key, value)

	db.commit()
	db.refresh(db_city)
	return db_city


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
	"""
	Удалить город (только для админов)
	"""
	db_city = db.query(models.City).filter(models.City.id == city_id).first()
	if db_city is None:
		raise HTTPException(status_code=404, detail="City not found")

	db.delete(db_city)
	db.commit()
	return {"detail": "Город успешно удален"}