from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# ✅ Allow CORS for Netlify + localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Set your OpenAI API key (Render → Environment Variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")

        if not prompt:
            return {"response": "⚠️ No prompt received"}

        # ✅ Call OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   # or "gpt-4" if available
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,          # limit length of response
            temperature=0.7          # creativity level
        )

        answer = response.choices[0].message["content"]
        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Backend error: {str(e)}"}
