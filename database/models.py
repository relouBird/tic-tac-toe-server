from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, text
# from database.dbHandler import Base
from typing import Annotated
from fastapi import Depends, HTTPException
import psycopg2
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from configuration.config import URL_DATABASE 
from sqlalchemy.orm import Session
from typing import List, Tuple



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

# element de remplissage de la table Users
class User_DB(Base):
    __tablename__ = "users"
    userToken = Column(String, index=True, primary_key=True)
    sub = Column(String,  index=True)
    email = Column(String, index=True)
    username = Column(String, index=True)
    expireTokenTime = Column(BigInteger, index=True)

# modele qui represente un jeu   
class Games(Base):
    __tablename__= "games"
    game_id = Column(String, primary_key=True, index=True)
    first_user_token = Column(String, index=True)
    second_user_token = Column(String, index=True)

# pas encore fonctionnel  
class User_LoggedIn(Base):
    __tablename__ = "logged_in"
    user_token = Column(String, primary_key=True, index=True)

# fonction qui permet de creer une table à partir d'un nom personnalisé
def createGameTable(game_id: str):
    with engine.connect() as connection:
        try:
            connection.execute(text("CREATE TABLE IF NOT EXISTS game_{} ( id SERIAL PRIMARY KEY,gid varchar(255) NOT NULL, jeu SERIAL NOT NULL)".format(game_id)))
            connection.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# fonction qui permet de recuperer une table à partir d'un nom personnalisé       
def getGameTable(game_id: str):
    with engine.connect() as connection:
        try:
            all_data : List[Tuple[str,int]] = []
            data = connection.execute(text("SELECT * FROM game_{}".format(game_id))).fetchall()
            if not data:
                return all_data
            for record in data:
                    partial = (record[1],record[2])
                    all_data.append(partial)
            return all_data  
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# fonction qui permet d'ajouter une donnée dans une table personnalisée
def addDataToGameTable(game_id: str,tour : Tuple[str,int]):
    (user_token,numberPlayed) = tour[0],tour[1]
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO game_{} (gid,jeu) VALUES ('{}',{})".format(game_id, user_token, numberPlayed)))
            connection.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    
