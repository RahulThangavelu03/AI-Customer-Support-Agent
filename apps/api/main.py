from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent

app = FastAPI()






class ChatRequest(BaseModel):

    message:str


@app.get("/health")
def get_health():

    return {"status":"ok"}


@app.post("/chat")
def chat_with_agent(input:ChatRequest):

    answer = run_agent(input.message)

    return{

        "response":answer
    }


