# definition des types de données
from pydantic import BaseModel

# classe qui definit le type d'utilisateur entrant
class User_DB(BaseModel):
    sub: int
    email: str
    username: str
    googleToken: str
    
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