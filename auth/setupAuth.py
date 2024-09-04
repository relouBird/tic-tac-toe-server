from typing import Annotated, Tuple
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

URL_DATABASE_POSTGRESQL = 'postgresql://postgres:relou123@localhost:5432/tictactoe'
engine = create_engine(URL_DATABASE_POSTGRESQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserTested(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
        

def fake_decode_token(token: str) -> UserTested:
    return UserTested(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
    
# lancement de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Annotated[Session,Depends(get_db)]) -> Tuple[UserTested, Session]:
    user = fake_decode_token(token)
    return db,user


# #endpoint test pour gerer la connexion avec token, mot de passe et username
# @app.get("/items/")
# async def read_items(user_and_db: Annotated[Tuple[UserTested, Session], Depends(get_current_user)]):
#     user, db = user_and_db
#     return {"user": user, "db": db}