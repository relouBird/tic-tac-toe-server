import fastapi
from fastapi.middleware.cors import CORSMiddleware
from configuration.config import GPT_API_KEY
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

app = fastapi.FastAPI()
apiKey = GPT_API_KEY
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    # Ajoutez d'autres origines si nécessaire
]

client = OpenAI(api_key=apiKey)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataModel(BaseModel):
    key1: str
    key2: str

class DataGpt(BaseModel):
    data: str

@app.get("/")
async  def root():
    return {"message":"hello"}

@app.post("/data")
async def get_data(data: DataModel):
    print("POST /data received:", data)
    return {"received": "data receive"}

@app.post("/message")
async def get_data(data: DataGpt):
    print("POST /data received:", data)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": data.data
        }
        ]
    )
    print(completion.choices[0].message)
    return {"received": completion.choices[0].message}

# Démarrage du serveur avec uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)