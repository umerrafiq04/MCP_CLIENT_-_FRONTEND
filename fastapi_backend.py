from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from client.app import run_model

app = FastAPI()

class ChatRequest(BaseModel):
    messages: List[Dict]  # full conversation


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    result = await run_model(request.messages)
    return {"response": result}
