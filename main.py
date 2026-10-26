from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM") 
EXPIRATION_ACCESS_TOKEN = int(os.getenv("EXPIRATION_ACCESS_TOKEN"))
EXPIRATION_REFRESH_TOKEN = int(os.getenv("EXPIRATION_REFRESH_TOKEN"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from orders_routes import orders_router
from products_routes import products_router

app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(products_router)

#Para executar uvicorn main:app --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port="8000", reload=True)