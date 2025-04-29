from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..utils.security import get_current_user, get_admin_user, get_city_manager

router = APIRouter()


@router.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db), city_id: Optional[int] = None, skip: int = 0, limit: int = 100):
	"""
	Получить список товаров, с возможностью фильтрации по городу
	"""
	query = db.query(models.Product).filter(models.Product.is_available == True)

	if city_id:
		# Показываем товары для конкретного города + товары доступные во всех городах
		query = query.filter((models.Product.city_id == city_id) | (models.Product.city_id == None))

	products = query.offset(skip).limit(limit).all()
	return products


@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
	"""
	Получить информацию о товаре по ID
	"""
	product = db.query(models.Product).filter(models.Product.id == product_id).first()
	if product is None:
		raise HTTPException(status_code=404, detail="Product not found")
	return product


@router.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db),
				   current_user: models.User = Depends(get_current_user)):
	"""
	Создать новый товар (для админа или менеджера города)
	"""
	# Проверка прав доступа для менеджера города
	if current_user.role != "admin" and product.city_id and product.city_id != current_user.city_id:
		raise HTTPException(status_code=403, detail="Not enough permissions for this city")

	db_product = models.Product(**product.dict())
	db.add(db_product)
	db.commit()
	db.refresh(db_product)
	return db_product


@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db),
				   current_user: models.User = Depends(get_current_user)):
	"""
	Обновить информацию о товаре
	"""
	db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
	if db_product is None:
		raise HTTPException(status_code=404, detail="Product not found")

	# Проверка прав доступа
	if current_user.role != "admin":
		if db_product.city_id and db_product.city_id != current_user.city_id:
			raise HTTPException(status_code=403, detail="Not enough permissions for this product")
		if product.city_id and product.city_id != current_user.city_id:
			raise HTTPException(status_code=403, detail="Cannot assign product to another city")

	for key, value in product.dict().items():
		setattr(db_product, key, value)

	db.commit()
	db.refresh(db_product)
	return db_product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db),
				   current_user: models.User = Depends(get_current_user)):
	"""
	Удалить товар
	"""
	db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
	if db_product is None:
		raise HTTPException(status_code=404, detail="Product not found")

	# Проверка прав доступа
	if current_user.role != "admin" and db_product.city_id and db_product.city_id != current_user.city_id:
		raise HTTPException(status_code=403, detail="Not enough permissions for this product")

	db.delete(db_product)
	db.commit()
	return {"detail": "Product deleted successfully"}
