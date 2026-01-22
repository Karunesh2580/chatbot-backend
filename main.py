from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.get("/")
async def root():
    return {"message": "Backend is running! Use POST /chat"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"response": "⚠️ No prompt received"}

    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 200
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return {"response": f"⚠️ OpenAI API error: {response.status_code} {response.text}"}

        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()

        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Request failed: {str(e)}"}
