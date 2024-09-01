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

    
class FacebookUser(BaseModel):
    id: str
    email: str
    name : str
    picture: str
    token: str
    expireTokenTime: int
    
#  class qui represente les données recues par la requete de verification d'un user
class FormData(BaseModel):
    userToken: str
    expireTokenTime: str
    gameId: str