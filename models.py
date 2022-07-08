from ast import Str
from codecs import backslashreplace_errors
from email.policy import default
#from operator import index
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean,Column,Integer,String
from database import Base

#create table

class Users(Base):
    __tablename__ ="users"

    id = Column(Integer,primary_key=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    hased_password = Column(String)
    is_active = Column(Boolean,default=True)

    #todos = relationship("Todos",back_populates="owner")

class Todos(Base):
    __tablename__ ="todos"
    id = Column(Integer,primary_key=True)
    title = Column(String(256))
    description = Column(String(256))