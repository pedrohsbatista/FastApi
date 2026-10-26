from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, EXPIRATION_ACCESS_TOKEN, EXPIRATION_REFRESH_TOKEN
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/account")
async def post_conta(user_schema: UserSchema, session: Session = Depends(get_session)):    
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
       raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    user = User(user_schema.name, user_schema.email, bcrypt_context.hash(user_schema.password), user_schema.active, user_schema.admin)
    session.add(user)
    session.commit()
    return { "mensagem": "Usuário cadastrado com sucesso" }

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == login_schema.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email/Senha inválido")    

    if not bcrypt_context.verify(login_schema.password, user.password):
        raise HTTPException(status_code=400, detail="Email/Senha inválido")
   
    return { 
               "access_token": create_token(user.id, timedelta(minutes = EXPIRATION_ACCESS_TOKEN)),
               "refresh_token": create_token(user.id, timedelta(days = EXPIRATION_REFRESH_TOKEN)),
               "type_token": "Bearer"
            }    

@auth_router.post("/login-form")
async def login_form(form: OAuth2PasswordRequestForm =  Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == form.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email/Senha inválido")    

    if not bcrypt_context.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Email/Senha inválido")
   
    return { 
               "access_token": create_token(user.id, timedelta(minutes = EXPIRATION_ACCESS_TOKEN)),               
               "type_token": "Bearer"
            }    

@auth_router.get("/refresh")
async def refresh(user: User = Depends(verify_token)):
      return {
          "access_token": create_token(user.id, timedelta(minutes = EXPIRATION_ACCESS_TOKEN)),
          "type_token": "Bearer"
      }
    

def create_token(user_id, duration):
    expiration = datetime.now(timezone.utc) + duration

    payload = { "sub": str(user_id), "exp": expiration }

    return jwt.encode(payload, SECRET_KEY, ALGORITHM)  