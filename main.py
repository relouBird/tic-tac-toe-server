import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from authlib.integrations.starlette_client import OAuth,OAuthError
# from database.dbHandler import create_user,existing_user
import os
import database.models as models
from database.dbHandler import engine, SessionLocal, createUser, db_dependacy
from sqlalchemy.orm import Session
from configuration.classType import GoogleUser

# importation des api-key et secret
from configuration.config import CLIENT_ID,CLIENT_SECRET,PORT


# lancement
app = fastapi.FastAPI()
models.Base.metadata.create_all(bind= engine)

#permet au serveur d'afficher des page html creer dans le dossier templates
templates = Jinja2Templates(directory="templates")

#gerer la protection et les secrets de session
app.add_middleware(
    SessionMiddleware,
    secret_key=CLIENT_SECRET,
    session_cookie="your_session_cookie_name",  # Nom du cookie de session
    max_age=3600,  # Temps de vie des sessions en secondes
    same_site="lax",  # Ou "strict" ou "none" selon vos besoins
    https_only=False  # Mettez à True en production avec HTTPS
)

#permet de d'initialiser l'authentification ici avec google
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': "http://127.0.0.1:5000/auth"
    }
)

    
# # lancement de la base de données
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependacy = Annotated[Session,Depends(get_db)]

# endpoint de depart et ici affiche une page html d'accueil
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="home.html", context={"request":request})

#endpoint sur lequel on lance l'authentification 
@app.get("/login")
async def login(request : Request):
    redirect_uri = request.url_for('authDef')
    return await oauth.google.authorize_redirect(request, redirect_uri)


#endpoint qui gere la connexion avec google malgré qu'on ne la voit pas reellement
@app.get("/auth")
async def authDef(request: Request, db : db_dependacy):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuthError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valide credentials")
    
    user_info = token.get('userinfo')
    user = GoogleUser(**user_info)
    createUser(google_user=user,db=db,request=request)
    return {"data": user}

# lancement du code (pas forcement necessaire)
HOST = "127.0.0.1"
if __name__ == "__main__":
    uvicorn.run('main:app',host=HOST,port=int(PORT),reload=True)