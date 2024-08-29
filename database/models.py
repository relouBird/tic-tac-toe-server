from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from database.dbHandler import Base

# element de remplissage de la table Users
class User_DB(Base):
    __tablename__ = "users"
    sub = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    username = Column(String, index=True)
    googleToken = Column(String)
    