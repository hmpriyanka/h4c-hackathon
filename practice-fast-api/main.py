from fastapi import FastAPI
from models import Question, QuizRequest, QuizResponse

app = FastAPI()

@app.get("/hello")
def greet():
    return {"message": "Hello World from FastAPI!"}

@app.get("/quiz")
def get_all_quiz():
    return "All quiz"

@app.post("/quiz", response_model=QuizResponse)
def generate_quiz(request: QuizRequest):
    questions = []
    for i in range(request.num_questions):
        if request.type == "mcq":
            q = Question(
                question=f"MCQ question {i+1} on {request.topic}?",
                options=[f"Option A{i+1}", f"Option B{i+1}", f"Option C{i+1}", f"Option D{i+1}"],
                answer=f"Option A{i+1}"
            )

        elif request.type == "subjective":
            q = Question(
                question=f"Subjective question {i+1} on {request.topic}?",
                answer=f"Sample subjective answer {i+1}"
            )

        elif request.type == "hybrid":
            # Alternate between MCQ and Subjective
            if i % 2 == 0:
                q = Question(
                    question=f"MCQ question {i+1} on {request.topic}?",
                    options=[f"Option A{i+1}", f"Option B{i+1}", f"Option C{i+1}", f"Option D{i+1}"],
                    answer=f"Option A{i+1}"
                )
            else:
                q = Question(
                    question=f"Subjective question {i+1} on {request.topic}?",
                    answer=f"Sample subjective answer {i+1}"
                )

        questions.append(q)
    qr=QuizResponse(input=request, quiz=questions, time="5mins")
    print("response:",qr)
    return QuizResponse(input=request, quiz=questions, time="5mins")
