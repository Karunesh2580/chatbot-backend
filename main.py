from fastapi import FastAPI

# FastAPI object create करो
app = FastAPI()

# Root endpoint define करो
@app.get("/")
def read_root():
    return {"message": "Backend is live!"}
