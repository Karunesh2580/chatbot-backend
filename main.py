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
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        if not prompt:
            return {"response": "⚠️ No prompt received"}
        return {"response": f"You said: {prompt}"}
    except Exception as e:
        return {"response": f"⚠️ Backend error: {str(e)}"}
