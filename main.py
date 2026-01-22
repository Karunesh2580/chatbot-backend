from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

# ✅ Allow frontend (Netlify) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Hugging Face token (Render env variables में डालना होगा)
HF_TOKEN = os.getenv("HF_TOKEN")

# ✅ Valid Hugging Face model (router supported)
HF_MODEL = "gpt2"   # तुम चाहो तो इसे किसी और supported model से बदल सकते हो

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
        response = requests.post(
            f"https://router.huggingface.co/hf-inference/{HF_MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt},
            timeout=30
        )

        if response.status_code != 200:
            return {"response": f"⚠️ Hugging Face error: {response.status_code} {response.text}"}

        try:
            result = response.json()
        except Exception:
            return {"response": "⚠️ Failed to parse Hugging Face response"}

        if isinstance(result, list) and "generated_text" in result[0]:
            answer = result[0]["generated_text"]
        elif isinstance(result, dict) and "generated_text" in result:
            answer = result["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            answer = f"⚠️ Model error: {result['error']}"
        else:
            answer = str(result)

        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Request failed: {str(e)}"}
