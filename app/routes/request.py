from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

from ..database import get_db
from .. import models, schemas
from ..utils.security import get_current_user
from ..services import email, telegram

router = APIRouter()


async def notify_managers(db: Session, request_id: int):
	"""
	Отправляет уведомления менеджерам о новой заявке
	"""
	# Получаем заявку
	request = db.query(models.Request).filter(models.Request.id == request_id).first()
	if not request:
		return

	# Получаем город
	city = db.query(models.City).filter(models.City.id == request.city_id).first()
	if not city:
		return

	# Получаем менеджеров для этого города
	managers = db.query(models.User).filter(
		models.User.city_id == request.city_id,
		models.User.role == "manager",
		models.User.is_active == True
	).all()

	# Формируем текст уведомления
	subject = f"Новая заявка #{request.id} из города {city.name}"
	message = f"Поступила новая заявка #{request.id}\n\n"
	message += f"Клиент: {request.name}\n"
	message += f"Телефон: {request.phone}\n"
	if request.email:
		message += f"Email: {request.email}\n"
	message += f"Город: {city.name}\n"
	message += f"Сообщение: {request.message}\n"

	# Если указана услуга или товар, добавляем информацию
	if request.service_id:
		service = db.query(models.Service).filter(models.Service.id == request.service_id).first()
		if service:
			message += f"Услуга: {service.name}\n"

	if request.product_id:
		product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
		if product:
			message += f"Товар: {product.name}\n"

	# Отправляем уведомления всем менеджерам
	for manager in managers:
		# По email
		if manager.email:
			await asyncio.create_task(email.send_notification(
				recipient=manager.email,
				subject=subject,
				body=message
			))

		# В телеграм (если настроен)
		if manager.telegram_id:
			await asyncio.create_task(telegram.send_notification(
				chat_id=manager.telegram_id,
				message=f"<b>{subject}</b>\n\n{message}"
			))


@router.post("/requests", response_model=schemas.Request)
async def create_request(request: schemas.RequestCreate, background_tasks: BackgroundTasks,
						 db: Session = Depends(get_db)):
	"""
	Создать новую заявку от клиента
	"""
	# Проверяем существование города
	city = db.query(models.City).filter(models.City.id == request.city_id).first()
	if not city:
		raise HTTPException(status_code=404, detail="City not found")

	# Проверяем существование услуги, если указана
	if request.service_id:
		service = db.query(models.Service).filter(models.Service.id == request.service_id).first()
		if not service:
			raise HTTPException(status_code=404, detail="Service not found")

	# Проверяем существование товара, если указан
	if request.product_id:
		product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
		if not product:
			raise HTTPException(status_code=404, detail="Product not found")

	# Создаем заявку
	db_request = models.Request(**request.dict())
	db.add(db_request)
	db.commit()
	db.refresh(db_request)

	# Запускаем отправку уведомлений в фоне
	background_tasks.add_task(notify_managers, db, db_request.id)

	return db_request


@router.get("/requests", response_model=List[schemas.Request])
def get_requests(
		db: Session = Depends(get_db),
		current_user: models.User = Depends(get_current_user),
		city_id: Optional[int] = None,
		status: Optional[str] = None,
		skip: int = 0,
		limit: int = 100
):
	"""
	Получить список заявок (только для авторизованных пользователей)
	"""
	query = db.query(models.Request)

	# Фильтр по роли пользователя
	if current_user.role != "admin":
		# Менеджеры видят только заявки своего города
		query = query.filter(models.Request.city_id == current_user.city_id)
	elif city_id:
		# Админ может фильтровать по городу
		query = query.filter(models.Request.city_id == city_id)

	# Фильтр по статусу
	if status:
		query = query.filter(models.Request.status == status)

	# Сортировка по дате (новые сверху)
	query = query.order_by(models.Request.created_at.desc())

	requests = query.offset(skip).limit(limit).all()
	return requests


@router.get("/requests/{request_id}", response_model=schemas.Request)
def get_request(request_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
	"""
	Получить детали заявки по ID
	"""
	request = db.query(models.Request).filter(models.Request.id == request_id).first()
	if request is None:
		raise HTTPException(status_code=404, detail="Request not found")

	# Проверка доступа
	if current_user.role != "admin" and request.city_id != current_user.city_id:
		raise HTTPException(status_code=403, detail="Not enough permissions to view this request")

	return request


@router.put("/requests/{request_id}", response_model=schemas.Request)
def update_request_status(
		request_id: int,
		request_update: schemas.RequestUpdate,
		db: Session = Depends(get_db),
		current_user: models.User = Depends(get_current_user)
):
	"""
	Обновить статус заявки
	"""
	db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
	if db_request is None:
		raise HTTPException(status_code=404, detail="Request not found")

	# Проверка доступа
	if current_user.role != "admin" and db_request.city_id != current_user.city_id:
		raise HTTPException(status_code=403, detail="Not enough permissions to update this request")

	# Проверка статуса
	valid_statuses = ["new", "processing", "completed", "cancelled"]
	if request_update.status not in valid_statuses:
		raise HTTPException(status_code=400, detail=f"Invalid status. Valid options: {', '.join(valid_statuses)}")

	db_request.status = request_update.status
	db.commit()
	db.refresh(db_request)

	return db_request