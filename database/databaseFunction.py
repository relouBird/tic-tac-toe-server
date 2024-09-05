from cgitb import text
from configuration.classType import FacebookUser, GoogleUser, LoggedUser, SetOfGame
from .models import Base, User_DB, Games
from .models import db_dependacy, inspector
from starlette.requests import Request
import secrets
import string

# les fonctions utilitaires
#--------------------------------
# Celle ci permet de generer un id de maniere aleatoire
def genId(length = 10):
    car = string.ascii_letters + string.digits
    id = "".join(secrets.choice(car) for _ in range(length))
    return id

# cette fonction permet de creer un user a partir de ses identifiants Google
def createGoogleUser(google_user : GoogleUser, db: db_dependacy, request: Request):
    user_database = None
    if google_user:
        request.session['user'] = dict(google_user)
        existing = db.query(User_DB).filter(User_DB.sub == google_user.sub).first()
        if existing:
            return existing
        else:
            user_database = User_DB(sub=google_user.sub, email=google_user.email, username=google_user.name,userToken=google_user.at_hash, expireTokenTime = google_user.exp)
            db.add(user_database)
            db.commit()
            db.refresh(user_database)
    
    return user_database

# cette fonction permet de creer un user a partir de ses identifiants Facebook
def createFacebookUser(facebook_user: FacebookUser, db: db_dependacy, request: Request):
    user_database = None
    if facebook_user:
        request.session['user'] = dict(facebook_user)
        existingUser = db.query(User_DB).filter(User_DB.sub == facebook_user.id).first()
        if existingUser:
            return existingUser
        else:
            user_database = User_DB(sub=facebook_user.id, email=facebook_user.email, username=facebook_user.name, userToken=facebook_user.token, expireTokenTime = facebook_user.expireTokenTime)
            db.add(user_database)
            db.commit()
            db.refresh(user_database)

    return user_database

# Ne fonctionne pas encore mais devrait permettre de creer un utilisateur a partir de ses identifiants Email et password
def createLoggedInUser(user_loggedIn: LoggedUser, db: db_dependacy, request : Request):
    user_database = None
    if user_loggedIn:
        request.session['user'] = dict(user_loggedIn)
        existingUser = db.query(User_DB).filter(User_DB.sub == user_loggedIn.id).first()
        if existingUser:
            return existingUser
        else:
            user_database = User_DB(sub=user_loggedIn.id, email=user_loggedIn.email, username=user_loggedIn.name, userToken=user_loggedIn.hashed_password, expireTokenTime = 1545445455644864)
            db.add(user_database)
            db.commit()
            db.refresh(user_database)

    return user_database    

# permet de verifier si un utilisateur est deja dans la base de données à partir de son id  
def getUserById(user_id: str, db: db_dependacy) -> User_DB:
    existing = db.query(User_DB).filter(User_DB.sub == user_id).first()
    if not existing:
        return None
    return existing

# permet de verifier si un utilisateur est deja dans la base de données à partir de son token  
def getUserByToken(user_token: str, db: db_dependacy) -> User_DB:
    existing = db.query(User_DB).filter(User_DB.userToken == user_token).first()
    if not existing:
        return None
    return existing

# permet de recuperer un jeu en fonction de id 
def getGame(game_id: str, db: db_dependacy) -> Games:
    existingGame = db.query(Games).filter(Games.game_id == game_id).first()
    if not existingGame:
        return None
    # retourne la partie en question
    return existingGame

# permet de recuperer les données table de jeu en fonction de son nom
# def getGameTable(game_id: str, db: db_dependacy):
#     # existingDataGameList = db.query(Base.metadata.tables["game_{}".format(game_id)]).all()
    
#     schemas = inspector.get_schema_names()

#     for schema in schemas:
#         print("schema: %s" % schema)
#         for table_name in inspector.get_table_names(schema=schema):
#             for column in inspector.get_columns(table_name, schema=schema):
#                 print("Column: %s" % column)

#     # all_data : List[Tuple[str,int]] = []
#     # if not existingDataGameList:
#     #     return all_data
#     # for dataTable in existingDataGameList:
#     #     partial = (dataTable["id"],dataTable["jeu"])
#     #     all_data.append(partial)
#     # # retourne la partie en question
#     # return all_data

# permet de creer un jeu a partir de l'id d'un createur
def createGame(creator: str, db: db_dependacy) -> Games:
    gid = genId(24)
    game_data = Games(game_id=gid, first_user_token=creator, second_user_token="")
    # table_game_data = createGameTableById(game_id=game_data.game_id)
    db.add(game_data)
    # db.add(table_game_data)
    db.commit()
    db.refresh(game_data)
    # retourne la partie en question
    return game_data

# permet de mettre a jour les données d'un jeu en cours generalement pour ajouter le 2eme joueurs
def updateGame(game_id: str, second_player_token: str, db: db_dependacy) -> Games:
    existingGame = db.query(Games).filter(Games.game_id == game_id).first()
    if not existingGame:
        return None
    # retourne la partie en question
    db.query(Games).filter(Games.game_id == game_id).update({Games.second_user_token : second_player_token})
    db.commit()
    existingGame = db.query(Games).filter(Games.game_id == game_id).first()
    return existingGame

def searchTable():
    pass