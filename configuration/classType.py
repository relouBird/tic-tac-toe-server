# definition des types de données
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

#  class qui represente les données recues par la requete de verification d'un user
class FormData(BaseModel):
    userToken: str
    expireTokenTime: int
    gameId: str