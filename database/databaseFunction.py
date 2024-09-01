from configuration.classType import FacebookUser, GoogleUser
from .models import User_DB, Games
from .models import db_dependacy
from starlette.requests import Request

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
       

# permet de verifier si un utilisateur est deja dans la base de données à partir de son token  
def getUser(user_id: str, db: db_dependacy):
    existing = db.query(User_DB).filter(User_DB.sub == user_id).first()
    if existing:
        return existing
    return None

def getGame(game_id: str, db: db_dependacy):
    existingGame = db.query(Games).filter(Games.game_id == game_id).first()
    if not existingGame:
        return None
    # retourne la partie en question
    return existingGame