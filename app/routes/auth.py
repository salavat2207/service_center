from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..config import settings
from .. import models, schemas
from ..utils.security import authenticate_user, create_access_token, get_password_hash, get_admin_user

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username, "role": user.role, "city_id": user.city_id},
		expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),
				current_user: models.User = Depends(get_admin_user)):
	# Проверка, существует ли пользователь
	db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
	db_user_email = db.query(models.User).filter(models.User.email == user.email).first()

	if db_user_username:
		raise HTTPException(status_code=400, detail="Username already registered")
	if db_user_email:
		raise HTTPException(status_code=400, detail="Email already registered")

	# Хешируем пароль
	hashed_password = get_password_hash(user.password)

	# Создаем нового пользователя
	db_user = models.User(
		username=user.username,
		email=user.email,
		hashed_password=hashed_password,
		city_id=user.city_id,
		role=user.role,
		is_active=user.is_active,
		telegram_id=user.telegram_id
	)

	db.add(db_user)
	db.commit()
	db.refresh(db_user)

	return db_user