import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# initialise le serveur
app = fastapi.FastAPI()

# tout les liens d'acces au front
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    # Ajoutez d'autres origines si nécessaire
]

# permet de donner les acces au front si tu as meme 12 fronts ajoute seulement
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# endpoint tu fais seulement la requete dans le front sur le localhost:5000 parce que jai mit 5000 comme port 
# et je demarre aussi sur le port 5000
@app.get('/')
async def root():
    return {"start":"welcome"}

# pour lancer
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=5000)