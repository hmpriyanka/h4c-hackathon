from fastapi import FastAPI, HTTPException
from models import QuizRequest, QuizResponse, Question
from dotenv import load_dotenv
import os
from openai import OpenAI
import json

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="Moodle Quiz Microservice")

@app.get("/hello")
def greet():
    return {"message": "Hello World from FastAPI!"}


@app.post("/quiz", response_model=QuizResponse)
def generate_quiz(request: QuizRequest):
    """
    Generate a quiz using OpenAI GPT (1.x Python API)
    """
    try:
        # Build prompt
        prompt = f"""
        Create {request.num_questions} quiz questions on the topic '{request.topic}'.
        Difficulty: {request.level.value}.
        Quiz type: {request.type.value}.
        Provide output in strict JSON format as a list of objects:
        [
            {{
                "question": "...",
                "answer": "...",
                "options": ["...", "..."]  // only for MCQs
            }}
        ]
        """

        # Call OpenAI API (1.x)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text_response = response.choices[0].message.content

        # Parse JSON returned by GPT
        try:
            quiz_list = json.loads(text_response)
            questions = []
            for q in quiz_list:
                questions.append(Question(
                    question=q.get("question"),
                    answer=q.get("answer"),
                    options=q.get("options")
                ))
        except json.JSONDecodeError:
            # fallback if GPT output is invalid JSON
            questions = []
            for i in range(request.num_questions):
                if request.type == "mcq":
                    q = Question(
                        question=f"Sample MCQ {i+1} on {request.topic}?",
                        answer="Option A",
                        options=["Option A", "Option B", "Option C", "Option D"]
                    )
                elif request.type == "subjective":
                    q = Question(
                        question=f"Sample subjective {i+1} on {request.topic}?",
                        answer="Sample answer"
                    )
                else:  # hybrid
                    if i % 2 == 0:
                        q = Question(
                            question=f"Sample MCQ {i+1} on {request.topic}?",
                            answer="Option A",
                            options=["Option A", "Option B", "Option C", "Option D"]
                        )
                    else:
                        q = Question(
                            question=f"Sample subjective {i+1} on {request.topic}?",
                            answer="Sample answer"
                        )
                questions.append(q)

        return QuizResponse(
            input=request,
            quiz=questions,
            time=f"{request.num_questions * 2} mins"  # example: 2 mins per question
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
