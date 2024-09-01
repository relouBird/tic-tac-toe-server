import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated
import requests
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from authlib.integrations.starlette_client import OAuth,OAuthError
import os
import database.models as models
from database.models import engine, SessionLocal, db_dependacy
from database.databaseFunction import createGoogleUser, createFacebookUser, getGame, getUser
from sqlalchemy.orm import Session
from configuration.classType import FormData, GoogleUser, FacebookUser

# importation des api-key et secret
from configuration.config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,PORT,FACEBOOK_CLIENT_ID,FACEBOOK_CLIENT_SECRET, BACKEND_URL

# lancement
app = fastapi.FastAPI()
models.Base.metadata.create_all(bind= engine)

#permet au serveur d'afficher des page html creer dans le dossier templates
templates = Jinja2Templates(directory="templates")

#gerer la protection et les secrets de session
app.add_middleware(
    SessionMiddleware,
    secret_key=GOOGLE_CLIENT_ID,
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
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': "http://127.0.0.1:5000/auth/google"
    }
)

# Ajout de l'authentification avec Facebook
oauth.register(
    name="facebook",
    client_id=FACEBOOK_CLIENT_ID,  # Remplacez par votre App ID
    client_secret=FACEBOOK_CLIENT_SECRET,  # Remplacez par votre App Secret
    authorize_url="https://www.facebook.com/dialog/oauth",
    authorize_params=None,
    access_token_url="https://graph.facebook.com/oauth/access_token",
    access_token_params=None,
    client_kwargs={'scope': 'email'},
    redirect_uri=f"{BACKEND_URL}/auth/facebook"
)

# endpoint de depart et ici affiche une page html d'accueil
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="home.html", context={"request":request})

#endpoint sur lequel on lance l'authentification Google 
@app.get("/login/google")
async def googleLogin(request : Request):
    redirect_uri = request.url_for('authDefGoogle')
    return await oauth.google.authorize_redirect(request, redirect_uri)

#endpoint sur lequel on lance l'authentification Facebook
@app.get("/login/facebook")
async def facebookLogin(request : Request):
    redirect_uri_facebook = request.url_for('authDefFacebook')
    return await oauth.facebook.authorize_redirect(request, redirect_uri_facebook)


#endpoint qui gere la connexion avec google malgré qu'on ne la voit pas reellement
@app.get("/auth/google")
async def authDefGoogle(request: Request, db : db_dependacy):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuthError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valide credentials")
    
    user_info = token.get('userinfo')
    user = GoogleUser(**user_info)
    bool_exist = False
    is_exist = getUser(user_id=user.sub, db=db)
    if is_exist:
        bool_exist = True
        user_database = is_exist
    else:
        user_database = createGoogleUser(google_user=user,db=db,request=request)
    
    # return RedirectResponse(f"{FRONTEND_URL}/home?user_token={user_database.user}")
    return {'data': user_database, 'is_exist': bool_exist}

#endpoint qui gere la connexion avec facebook malgré qu'on ne la voit pas reellement
@app.get("/auth/facebook")
async def authDefFacebook(request: Request, db : db_dependacy):
    try:
        token = await oauth.facebook.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuthError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valide credentials")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")
    access_token = token['access_token']
    expire_access_token = token['expires_at']

        # Faire une requête à l'API Graph de Facebook pour obtenir des informations utilisateur
    user_info_url = 'https://graph.facebook.com/me'
    user_info_params = {
            'access_token': access_token,
            'fields': 'id,name,email,picture'
        }

    user_info_response = requests.get(user_info_url, params=user_info_params)
    user_info_response.raise_for_status()  # Lever une exception si la requête échoue

    user_info = user_info_response.json()  # Décoder la réponse JSON
    user = FacebookUser(id=user_info['id'], name=user_info['name'], email=user_info['email'], picture=user_info['picture']['data']['url'], token=access_token, expireTokenTime=expire_access_token)
    is_exist = getUser(user_id=user.sub, db=db)
    bool_exist = False
    if is_exist:
        bool_exist = True
        user_database = is_exist
    else:
        user_database= createFacebookUser(facebook_user=user, db=db, request=request)
    return {'data': user_database, 'is_exist': bool_exist}
    

#endpoint qui permet de verifier si un utilisateur est conncté ou pas et de le renvoyer vers la connexion sinon...
# @app.post('game-verification')
# async def userVerification(request: Request, db: db_dependacy, form_data : FormData):
#     user_data = getUser(user_token=form_data.userToken, db=db)
#     if user_data:
#         game_data = getGame(game_id = form_data.gameId, db=db)
#         if game_data.first_user_token == user_data.userToken:
#             pass
#         else:
#             return RedirectResponse(f"{FRONTEND_URL}/friend-games/launch?user_token={user_data.user}&game_id={form_data.gameId}")
#     else:
#         redirect_uri = request.url_for('login')
#         return RedirectResponse(redirect_uri)
    

# lancement du code (pas forcement necessaire)
HOST = "127.0.0.1"
if __name__ == "__main__":
    uvicorn.run('main:app',host=HOST,port=int(PORT),reload=True)