# definition des types de données
from typing import List, Tuple
from pydantic import BaseModel

    
# class qui represente toutes les informations envoyées par google pour representer un utilisateur 
class GoogleUser(BaseModel):
    iss : str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: str
    family_name: str
    iat: int
    exp: int

# class qui represente toutes les informations dont j'ai besoin pour utilisateur de facebook pour representer un utilisateur    
class FacebookUser(BaseModel):
    id: str
    email: str
    name : str
    picture: str
    token: str
    expireTokenTime: int

# pas encore pret.................... 
class LoggedUser(BaseModel):
    id: str
    email: str
    name: str
    hashed_password: str
    
#  class qui represente les données recues par la requete de verification d'un user
class FormData(BaseModel):
    userToken: str
    expireTokenTime: int
    gameId: str

# classe qui definit la structure d'un jeu...  
class GameData(BaseModel):
    gameId : str
    first_user_token : str
    second_user_token : str
    tours : List[Tuple[str,int]]
    

# classe qui definit le type de retour dans la creation d'un jeu avec AI
class GameDataWithAI(BaseModel):
    url: str
    id: str
    token : str
    
type GameTableDataType = List[Tuple[str,int]]

class SetOfGame(BaseModel):
    id: str
    jeu: int