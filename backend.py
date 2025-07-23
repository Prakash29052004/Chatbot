import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return JSONResponse(status_code=500, content={"error": "GEMINI_API_KEY environment variable not set."})
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": chat_request.message}]}
        ]
    }
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={api_key}",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            # Safer extraction of answer
            try:
                answer = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                return JSONResponse(status_code=500, content={"error": "Unexpected response format from Gemini API.", "raw_response": data})
            return {"response": answer}
        else:
            return JSONResponse(status_code=500, content={"error": response.text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 