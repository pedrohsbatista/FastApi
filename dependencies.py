from fastapi import HTTPException, Depends
from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt
from main import SECRET_KEY, ALGORITHM, auth_schema

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(auth_schema), session: Session = Depends(get_session)):
  try:
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)    
    return session.query(User).filter(User.id == int(payload.get("sub"))).first()
  except:
      raise HTTPException(status_code=401, detail="Acesso Negado")