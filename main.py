from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "mistralai/Mistral-7B-Instruct"

# Local pipeline (example: distilGPT2)
local_pipeline = pipeline("text-generation", model="distilgpt2")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    mode = data.get("mode", "huggingface")  # default Hugging Face

    if mode == "huggingface":
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt}
        )
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            answer = result[0]["generated_text"]
        else:
            answer = str(result)
        return {"response": answer}

    elif mode == "local":
        result = local_pipeline(prompt, max_length=100, num_return_sequences=1)
        answer = result[0]["generated_text"]
        return {"response": answer}

    else:
        return {"response": "⚠️ Invalid mode selected"}
