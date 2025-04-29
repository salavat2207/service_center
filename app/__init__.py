import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app import models
from app.database import SessionLocal, engine, Base
from app.utils.security import get_password_hash


def init_db():
	# Создаем таблицы
	Base.metadata.create_all(bind=engine)

	# Открываем сессию
	db = SessionLocal()

	try:
		# Проверяем, есть ли уже данные в базе
		city_count = db.query(models.City).count()
		user_count = db.query(models.User).count()

		if city_count == 0:
			# Добавляем города
			print("Добавляем города...")
			cities = [
				models.City(name="Челябинск", active=True),
				models.City(name="Екатеринбург", active=True),
				models.City(name="Магнитогорск", active=True)
			]
			db.add_all(cities)
			db.commit()

			for city in cities:
				print(f"  - Добавлен город: {city.name} (ID: {city.id})")

		if user_count == 0:
			# Добавляем администратора
			print("Добавляем администратора...")
			admin = models.User(
				username="admin",
				email="admin@example.com",
				hashed_password=get_password_hash("admin123"),
				city_id=1,  # Москва
				role="admin",
				is_active=True
			)
			db.add(admin)

			# Добавляем менеджеров для каждого города
			print("Добавляем менеджеров для городов...")
			managers = [
				models.User(
					username="manager_msk",
					email="manager_msk@example.com",
					hashed_password=get_password_hash("manager123"),
					city_id=1,  # Москва
					role="manager",
					is_active=True
				),
				models.User(
					username="manager_spb",
					email="manager_spb@example.com",
					hashed_password=get_password_hash("manager123"),
					city_id=2,  # Санкт-Петербург
					role="manager",
					is_active=True
				),
				models.User(
					username="manager_nsk",
					email="manager_nsk@example.com",
					hashed_password=get_password_hash("manager123"),
					city_id=3,  # Новосибирск
					role="manager",
					is_active=True
				)
			]
			db.add_all(managers)
			db.commit()

			print(f"  - Добавлен администратор: {admin.username} (ID: {admin.id})")
			for manager in managers:
				print(f"  - Добавлен менеджер: {manager.username} для города ID: {manager.city_id}")

			# Добавляем примеры товаров
			print("Добавляем примеры товаров...")
			products = [
				models.Product(
					name="Смартфон Samsung Galaxy",
					description="Флагманский смартфон с отличной камерой",
					price=49999.99,
					is_available=True,
					city_id=None  # Доступен во всех городах
				),
				models.Product(
					name="Ноутбук ASUS",
					description="Мощный ноутбук для работы и игр",
					price=79999.99,
					is_available=True,
					city_id=None  # Доступен во всех городах
				),
				models.Product(
					name="Планшет Apple iPad",
					description="Планшет с отличным экраном и производительностью",
					price=39999.99,
					is_available=True,
					city_id=1  # Только в Москве
				)
			]
			db.add_all(products)
			db.commit()

			for product in products:
				print(f"  - Добавлен товар: {product.name} (ID: {product.id})")

			# Добавляем примеры услуг
			print("Добавляем примеры услуг...")
			services = [
				models.Service(
					name="Замена экрана смартфона",
					description="Профессиональная замена экрана с гарантией",
					price=3000.00,
					estimated_time="1-2 часа",
					is_available=True,
					city_id=None  # Доступна во всех городах
				),
				models.Service(
					name="Чистка ноутбука от пыли",
					description="Полная разборка и чистка системы охлаждения",
					price=2000.00,
					estimated_time="1 час",
					is_available=True,
					city_id=None  # Доступна во всех городах
				),
				models.Service(
					name="Восстановление данных",
					description="Восстановление данных с поврежденных носителей",
					price=5000.00,
					estimated_time="1-3 дня",
					is_available=True,
					city_id=1  # Только в Москве
				)
			]
			db.add_all(services)
			db.commit()

			for service in services:
				print(f"  - Добавлена услуга: {service.name} (ID: {service.id})")

		print("Инициализация базы данных завершена!")

	finally:
		db.close()


if __name__ == "__main__":
	init_db()