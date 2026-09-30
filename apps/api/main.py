from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent

app = FastAPI()





from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import run_agent


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class ChatRequest(BaseModel):

    message:str


@app.get("/health")
def get_health():

    return {"status":"ok"}


@app.post("/chat")
def chat_with_agent(input:ChatRequest):

    result = run_agent(input.message)

    return result

    


