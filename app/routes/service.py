from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..utils.security import get_current_user, get_admin_user, get_city_manager

router = APIRouter()
@router.get("/services", response_model=List[schemas.Service])


def get_services(db: Session = Depends(get_db), city_id: Optional[int] = None, skip: int = 0, limit: int = 100):
	"""
	Получить список услуг, с возможностью фильтрации по городу
	"""
	query = db.query(models.Service).filter(models.Service.is_available == True)

	if city_id:
		# Показываем услуги для конкретного города + услуги доступные во всех городах
		query = query.filter((models.Service.city_id == city_id) | (models.Service.city_id == None))

	services = query.offset(skip).limit(limit).all()
	return services


@router.get("/services/{service_id}", response_model=schemas.Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
	"""
	Получить информацию об услуге по ID
	"""
	service = db.query(models.Service).filter(models.Service.id == service_id).first()
	if service is None:
		raise HTTPException(status_code=404, detail="Service not found")
	return service


@router.get("/services/{service_id}", response_model=schemas.Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
	"""
	Получить информацию об услуге по ID
	"""
	service = db.query(models.Service).filter(models.Service.id == service_id).first()
	if service is None:
		raise HTTPException(status_code=404, detail="Service not found")
	return service


@router.post("/services", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db),
				   current_user: models.User = Depends(get_current_user)):
	"""
	Создать новую услугу (для админа или менеджера города)
	"""
	# Проверка прав доступа для менеджера города
	if current_user.role != "admin" and service.city_id and service.city_id != current_user.city_id:
		raise HTTPException(status_code=403, detail="Not enough permissions for this city")

	db_service = models.Service(**service.dict())
	db.add(db_service)
	db.commit()
	db.refresh(db_service)
	return db_service


@router.put("/services/{service_id}", response_model=schemas.Service)
def update_service(service_id: int, service: schemas.ServiceCreate, db: Session = Depends(get_db),
				   current_user: models.User = Depends(get_current_user)):
	"""
	Обновить информацию об услуге
	"""
	db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
	if db_service is None:
		raise HTTPException(status_code=404, detail="Service not found")

	# Проверка прав доступа
	if current_user.role != "admin":
		if db_service.city_id and db_service.city_id != current_user.city_id:
			raise HTTPException(status_code=403, detail="Not enough permissions for this service")
		if service.city_id and service.city_id != current_user.city_id:
			raise HTTPException(status_code=403, detail="Cannot assign service to another city")

	for key, value in service.dict().items():
		setattr(db_service, key, value)

	db.commit()
	db.refresh(db_service)
	return db_service



@router.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db),
				   current_user: models.User = Depends(get_current_user)):
	"""
	Удалить услугу
	"""
	db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
	if db_service is None:
		raise HTTPException(status_code=404, detail="Service not found")

	# Проверка прав доступа
	if current_user.role != "admin" and db_service.city_id and db_service.city_id != current_user.city_id:
		raise HTTPException(status_code=403, detail="Not enough permissions for this service")

	db.delete(db_service)
	db.commit()
	return {"detail": "Service deleted successfully"}