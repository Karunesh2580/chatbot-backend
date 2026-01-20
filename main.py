from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS allow करना जरूरी है
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Netlify और localhost दोनों से allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    return {"response": f"You said: {prompt}"}
