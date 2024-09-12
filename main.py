import time
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import requests
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from authlib.integrations.starlette_client import OAuth,OAuthError
import os
# from auth.setupAuth import UserTested, get_current_user
import database.models as models
from typing import Annotated, List, Tuple
from database.models import User_DB, engine, SessionLocal, db_dependacy, createGameTable, getGameTable, addDataToGameTable
from database.databaseFunction import createGoogleUser, createFacebookUser, getGame, createGame, createAIGame, updateGame, getUserByToken, getUserById
from database.tictactoeHandler import best_move, renderBoard
from configuration.classType import FormData, GameData, GameDataWithAI, GoogleUser, FacebookUser

# importation des api-key et secret
from configuration.config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,PORT,FACEBOOK_CLIENT_ID,FACEBOOK_CLIENT_SECRET, BACKEND_URL, FRONTEND_URL

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

# Ajoutez le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Autoriser votre frontend local
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
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
    is_exist = getUserById(user_id=user.sub, db=db)
    if is_exist:
        bool_exist = True
        user_database = is_exist
    else:
        user_database = createGoogleUser(google_user=user,db=db,request=request)
    
    return RedirectResponse(f"{FRONTEND_URL}/selectgame?user_token={user_database.userToken}")
    # return {'data': user_database, 'is_exist': bool_exist}

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
    is_exist = getUserById(user_id=user.id, db=db)
    bool_exist = False
    if is_exist:
        bool_exist = True
        user_database = is_exist
    else:
        user_database= createFacebookUser(facebook_user=user, db=db, request=request)
    # return {'data': user_database, 'is_exist': bool_exist}
    return RedirectResponse(f"{FRONTEND_URL}/selectgame?user_token={user_database.userToken}")
 

# endpoint qui permet de verifier si un utilisateur est conncté ou pas et de le renvoyer vers la connexion sinon...
@app.post('/game-settings')
async def gameSettings(request: Request, db: db_dependacy, form_data : FormData):
    user_data: User_DB = getUserByToken(user_token=form_data.userToken, db=db)
    game_data = getGame(game_id = form_data.gameId, db=db)
    print(user_data, game_data)
    # si le user est connecté il continue 
    if user_data:
        if game_data:
            if game_data.first_user_token == user_data.userToken:
                return {"gameId": game_data.game_id} # on retourne quand meme l'id de la partie
            else:
                # on redirige vers le front avec les bons identifiants
                game_data= updateGame(game_id=game_data.game_id, second_player_token= user_data.userToken , db=db)
                return {"redirect": f"{FRONTEND_URL}/game?user_token={user_data.userToken}&game_id={form_data.gameId}"}
        else:
            game_data = createGame(creator=user_data.userToken, db=db)
            return {"gameId": game_data.game_id} # on retourne l'id de la partie pour partager le lien
    # ici il est n'est pas connecté mais s'il y a l'id de la partie alors on l'a juste invité donc il faut le rediriger pour creer son 
    else:
        if game_data:
            # return {"redirect": f"{FRONTEND_URL}?game_id={form_data.gameId}"}
            return RedirectResponse(f"{FRONTEND_URL}?game_id={form_data.gameId}")
        
        else:
            # return {"redirect": f"{FRONTEND_URL}"}
            return RedirectResponse(f"{FRONTEND_URL}")

# ce endpoint permet de savoir si une autre personne a rejoint le lien d'invitation pour debuter la partie 
@app.post('/game-verification')
async def gameVerification(request: Request, db: db_dependacy, form_data : FormData):
    user_data: User_DB = getUserByToken(user_token=form_data.userToken, db=db)
    game_data = getGame(game_id = form_data.gameId, db=db)
    print(user_data, game_data)
    if user_data:
        if game_data:
            if game_data.second_user_token != "": # il y a un user et une partie en cours on verifie pour voir s'il y 'a un un second joueur
                createGameTable(game_id=game_data.game_id)
                # renvoi l'adresse pour lancer le jeu...
                return {"redirect": f"{FRONTEND_URL}/log.html?user_token={user_data.userToken}&game_id={form_data.gameId}"} # url a changer
            else:
                # il y' a pas toujours de second joueur
                return {"result": "waiting for a player..."}
        else:
            return {"result": "no game found."}
    else:
        if game_data:
            return {"redirect": f"{FRONTEND_URL}?game_id={form_data.gameId}"}
        else:
            return {"redirect": f"{FRONTEND_URL}"}

# ce endpoint permet de renvoyer les données du jeu en cours
@app.post("/get-gamedata")
async def getDataGame(request: Request, db: db_dependacy, dataGame : GameData):
    gameDataPlayed = getGameTable(game_id=dataGame.gameId)
    gameToSend = GameData(gameId=dataGame.gameId,first_user_token=dataGame.first_user_token,second_user_token=dataGame.second_user_token, tours=gameDataPlayed)
    print(gameToSend)
    return gameToSend

# ce endpoint permet de renvoyer les données du jeu en cours
@app.post("/update-gamedata")
async def updateDataGame(request: Request, db: db_dependacy, dataGames : GameData):
    gameDataPlayed = getGameTable(game_id=dataGames.gameId)
    difference = len(dataGames.tours) - len(gameDataPlayed)
    if difference == 1:
        addDataToGameTable(game_id=dataGames.gameId, tour=dataGames.tours[-1])
    elif difference == 0:
        pass
    elif difference < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error: game data is corrupted")
    return {"data": "send"}

# ce endpoint permet de lancer le jeu avec l'ia sur le menu de lancement de jeu
@app.post("/launch-ia-game")
async def launchGame(db: db_dependacy, form_data : FormData):
    user_data: User_DB = getUserByToken(user_token=form_data.userToken, db=db)
    if user_data:
        game_data = createAIGame(creator=user_data.userToken, db=db)
        print(user_data, game_data)
        createGameTable(game_id=game_data.game_id)
        redirectData = GameDataWithAI(url=f"{FRONTEND_URL}/game", id=game_data.game_id, token=user_data.userToken)
        return redirectData # url a changer
    else:
        # return RedirectResponse(f"{FRONTEND_URL}")
        return {"redirect": f"{FRONTEND_URL}"}

# ce endpoint permet de d'ajouter un donnée de jeu avec l'ia sur le menu de lancement de jeu
@app.post("/update-ia-game")
async def updateAIGame( db: db_dependacy, dataGames : GameData):
    gameDataPlayed = getGameTable(game_id=dataGames.gameId)
    difference = len(dataGames.tours) - len(gameDataPlayed)
    if difference == 1:
        addDataToGameTable(game_id=dataGames.gameId, tour=dataGames.tours[-1]) # ajoute ce que le joueur a fait
        board = renderBoard(tableData=dataGames.tours) # creer un tableau à partir des mouvements
        ia_move = best_move(board)
        ia_table: int = ia_move  +1
        tableEntry = "AI",ia_table
        board[ia_move] = "O"
        addDataToGameTable(game_id=dataGames.gameId, tour=tableEntry)
        gameDataPlayed = getGameTable(game_id=dataGames.gameId)
        newDataGames = GameData(gameId=dataGames.gameId, first_user_token=dataGames.first_user_token, second_user_token=dataGames.second_user_token, tours=gameDataPlayed)
        return newDataGames
    elif difference == 0:
        pass
    elif difference < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error: game data is corrupted")
    return {"data": dataGames}

# lancement du code (pas forcement necessaire)
HOST = "127.0.0.1"
if __name__ == "__main__":
    uvicorn.run('main:app',host=HOST,port=int(PORT),reload=True)