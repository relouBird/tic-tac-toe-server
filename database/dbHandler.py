from typing import Annotated
from fastapi import Depends
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configuration.classType import GoogleUser
from configuration.config import URL_DATABASE 
from sqlalchemy.orm import Session
import database.models as models
from starlette.requests import Request



URL_DATABASE_POSTGRESQL = URL_DATABASE
engine = create_engine(URL_DATABASE_POSTGRESQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# lancement de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# gerer la dependance de la session
db_dependacy = Annotated[Session,Depends(get_db)]
        



# cette fonction permet de creer un user a partir de ses identifiants Google
def createUser(google_user : GoogleUser, db: db_dependacy, request: Request):
    if google_user:
        request.session['user'] = dict(google_user)
        existing = db.query(models.User_DB).filter(models.User_DB.sub == google_user.sub).first()
    if existing:
        pass
    else:
        user_database = models.User_DB(sub=google_user.sub, email=google_user.email, username=google_user.name,googleToken=google_user.at_hash)
        db.add(user_database)
        db.commit()
        db.refresh(user_database)