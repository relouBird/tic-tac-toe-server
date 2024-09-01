from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
# from database.dbHandler import Base
from typing import Annotated
from fastapi import Depends
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configuration.config import URL_DATABASE 
from sqlalchemy.orm import Session



URL_DATABASE_POSTGRESQL = 'postgresql://postgres:relou123@localhost:5432/tictactoe'
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

# element de remplissage de la table Users
class User_DB(Base):
    __tablename__ = "users"
    sub = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    username = Column(String, index=True)
    userToken = Column(String, index=True)
    expireTokenTime = Column(BigInteger, index=True)
    
class Games(Base):
    __tablename__= "games"
    game_id = Column(String, primary_key=True, index=True)
    first_user_token = Column(String, index=True)
    second_user_token = Column(String, index=True)
    

# fonction qui cree un model de table dont le nom de la table sera le nom mit en parametre
def createGameTableById(game_id : str):
    class GameIdTable(Base):
        __tablename__ = game_id
        sub = Column(String, primary_key=True, index=True)
        numberPlayed = Column(Integer, index=True)
    return GameIdTable
    