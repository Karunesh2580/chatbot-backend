from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

# ✅ Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Hugging Face Token from Railway ENV
HF_TOKEN = os.getenv("HF_TOKEN")

# ✅ Working model
HF_MODEL = "distilgpt2"

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
        # ✅ Router endpoint
        url = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

        payload = {
            "inputs": prompt,
            "options": {"use_cache": False},
        }

        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return {"response": f"⚠️ Hugging Face error: {response.status_code} {response.text}"}

        result = response.json()

        # ✅ Extract text from response
        if isinstance(result, list) and "generated_text" in result[0]:
            answer = result[0]["generated_text"]
        elif isinstance(result, dict) and "generated_text" in result:
            answer = result["generated_text"]
        else:
            answer = str(result)

        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Request failed: {str(e)}"}
