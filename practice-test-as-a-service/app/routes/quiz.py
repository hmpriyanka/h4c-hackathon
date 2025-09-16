from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from ..services import openai_service

router = APIRouter()

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "medium"

class QuizResponse(BaseModel):
    questions: list

class EvalRequest(BaseModel):
    quiz: list
    responses: list

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(req: QuizRequest, x_api_key: str = Header(...)):
    if x_api_key != os.getenv("SERVICE_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    questions = await openai_service.generate_quiz(req.topic, req.num_questions, req.difficulty)
    return QuizResponse(questions=questions)

@router.post("/evaluate")
async def evaluate(req: EvalRequest, x_api_key: str = Header(...)):
    if x_api_key != os.getenv("SERVICE_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    result = await openai_service.evaluate_quiz(req.quiz, req.responses)
    return result
