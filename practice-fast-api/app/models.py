from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class QuizLevel(str, Enum):   # inherit str, so JSON works with string values
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuizType(str, Enum):
    SUBJECTIVE = "subjective"
    MCQ = "mcq"
    HYBRID = "hybrid"
class Question(BaseModel):
    question: str
    answer: str
    options: Optional[List[str]]=None

class QuizRequest(BaseModel):
    topic: str
    num_questions: int
    level: QuizLevel
    type: QuizType

class QuizResponse(BaseModel):
    input: QuizRequest
    quiz: List[Question]
    time: str