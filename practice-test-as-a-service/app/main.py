from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import quiz

app = FastAPI(title="AI Quiz Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])

@app.get("/health")
def health():
    return {"status": "ok"}

def greet():
    return "hello i am fast api"
