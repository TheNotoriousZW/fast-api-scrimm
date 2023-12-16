from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import database, models
from fastapi import Depends

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str) -> str:
    hash_password = pwd_context.hash(password)

    return hash_password

def hash_valid(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)
    
        



    