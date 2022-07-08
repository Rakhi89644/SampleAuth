from http.client import HTTPException
from lib2to3.pgen2 import token
from turtle import st
from fastapi import FastAPI,Depends
from database import SessionLocal
import models
import schemas
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timedelta
#from jose import jwt
#from ssl import _PasswordType


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    password : str
models.Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = '161dffeb2096e8a6d057944ce83d8d721cbac5efdd23173ab24e5d7d99dc65a5'
ALOGORITHUM = "HS256"

oAuth_bearer = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password,hash_password):
    return bcrypt_context.verify(plain_password,hash_password)
# it will take username and database
def authenticate_user(username:str,password:str,db):
    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
            .first()
    if not user:
        return False
    if not verify_password(password,user.hash_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expire_delta:Optional[timedelta]=None):
    encode = {"sub":username,"id":user_id}
    if expire_delta:
        expire = datetime.utcnow()+ timedelta(minutes=15)
        encode.update({"exp":expire})
        return jwt.encode(encode,SECRET_KEY,algorithm=ALOGORITHUM)



@app.post('/create/user')
async def create_new_user(create_user: CreateUser,db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.hashed_password = create_user.password
    create_user_model.is_active = True
   
    
    hash_password = get_password_hash(create_user.password)

    create_user_model.hased_password = hash_password
    db.add(create_user_model)
    db.commit()

@app.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                   db:Session = Depends(get_db)):
                                   user = authenticate_user(form_data.username,form_data.password,db)
                                   if not user:
                                    raise HTTPException(status_code=404,detail="User not found")
                                   return "User validated"
                                   token_expire = timedelta(minutes=20)
                                   token = create_access_token(user.username,user_id,expire_delta=token_expire)
                                   return {"token":token}