from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn

from .database import get_db, engine, Base
from .routes import city_router, product_router, service_router, request_router, admin_router, auth_router
from .models import user as user_models, city as city_models, product as product_models, service as service_models, request as request_models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service Center API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Подключаем роутеры
# app.include_router(auth_router.router, prefix="/api", tags=["auth"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(city_router, prefix="/api", tags=["cities"])
app.include_router(product_router, prefix="/api", tags=["products"])
app.include_router(service_router, prefix="/api", tags=["services"])
app.include_router(request_router, prefix="/api", tags=["requests"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Service Center API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)