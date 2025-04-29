from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..utils.security import get_admin_user
from ..utils.security import get_password_hash

router = APIRouter()

@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
    """
    Получить список всех пользователей (только для админов)
    """
    users = db.query(models.User).all()
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
    """
    Получить информацию о пользователе по ID (только для админов)
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserCreate, db: Session = Depends(get_db),
				current_user: models.User = Depends(get_admin_user)):
	"""
	Обновить информацию о пользователе (только для админов)
	"""
	db_user = db.query(models.User).filter(models.User.id == user_id).first()
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")

	# Проверка уникальности почты и имени пользователя
	if user_update.username != db_user.username:
		username_exists = db.query(models.User).filter(models.User.username == user_update.username).first()
		if username_exists:
			raise HTTPException(status_code=400, detail="Username already registered")

	if user_update.email != db_user.email:
		email_exists = db.query(models.User).filter(models.User.email == user_update.email).first()
		if email_exists:
			raise HTTPException(status_code=400, detail="Email already registered")









# # Обновляем данные
# from ..utils.security import get_password_hash
#
# # Обновляем все поля кроме пароля
# for key, value in user_update.dict(exclude={"password"}).items():
# 	setattr(db_user, key, value)
#
# # Обновляем пароль, если он был изменен
# if user_update.password:
# 	db_user.hashed_password = get_password_hash(user_update.password)
#
# db.commit()
# db.refresh(db_user)
# return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
	"""
	Удалить пользователя (только для админов)
	"""
	# Нельзя удалить самого себя
	if user_id == current_user.id:
		raise HTTPException(status_code=400, detail="Cannot delete yourself")

	db_user = db.query(models.User).filter(models.User.id == user_id).first()
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")

	db.delete(db_user)
	db.commit()
	return {"detail": "User deleted successfully"}


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
	"""
	Получить статистику по системе (только для админов)
	"""
	# Общая статистика
	total_products = db.query(models.Product).count()
	total_services = db.query(models.Service).count()
	total_requests = db.query(models.Request).count()
	total_users = db.query(models.User).count()
	total_cities = db.query(models.City).count()

	# Статистика по заявкам
	new_requests = db.query(models.Request).filter(models.Request.status == "new").count()
	processing_requests = db.query(models.Request).filter(models.Request.status == "processing").count()
	completed_requests = db.query(models.Request).filter(models.Request.status == "completed").count()
	cancelled_requests = db.query(models.Request).filter(models.Request.status == "cancelled").count()

	return {
		"total": {
			"products": total_products,
			"services": total_services,
			"requests": total_requests,
			"users": total_users,
			"cities": total_cities
		},
		"requests": {
			"new": new_requests,
			"processing": processing_requests,
			"completed": completed_requests,
			"cancelled": cancelled_requests
		}
	}