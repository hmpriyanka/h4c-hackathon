from app.utils import extract_json
from fastapi import FastAPI, HTTPException
from app.models import QuizRequest, QuizResponse, Question
import json
import ollama

app = FastAPI(title="Moodle Quiz Microservice (Ollama)")

@app.get("/hello")
def greet():
    return {"message": "Hello World from FastAPI + Ollama!"}


@app.post("/quiz", response_model=QuizResponse)
def generate_quiz(request: QuizRequest):
    """
    Generate a quiz using LLaMA2 via Ollama Python API
    """
    try:
        # Build prompt for Ollama
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
        print("DEBUG: Input prompt is:", prompt)

        # Call Ollama Python API (not subprocess)
        result = ollama.chat(
            model="llama2",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract text response
        print("DEBUG: Ollama raw response:", result)
        text_response = result["message"]["content"].strip()

        # Try parsing JSON
        try:
            clean_json = extract_json(text_response)
            quiz_list = json.loads(clean_json)
            questions = []
            for q in quiz_list:
                questions.append(Question(
                    question=q.get("question"),
                    answer=q.get("answer"),
                    options=q.get("options")
                ))
        except json.JSONDecodeError:
            # fallback → raise service error instead of dummy questions
            raise HTTPException(
                status_code=502,
                detail="Service issue: Ollama did not return valid JSON"
            )

        return QuizResponse(
            input=request,
            quiz=questions,
            time=f"{request.num_questions * 2} mins"  # example: 2 mins per Q
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
