import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_quiz(topic: str, num_questions: int, difficulty: str):
    prompt = f"Generate {num_questions} multiple-choice questions on {topic} with difficulty {difficulty}. Provide JSON with fields: question, options, answer."
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    try:
        content = response.choices[0].message["content"]
        return json.loads(content)
    except Exception as e:
        return [{"error": str(e), "raw": response}]

async def evaluate_quiz(quiz: list, responses: list):
    score = 0
    feedback = []
    for q, r in zip(quiz, responses):
        correct = (q.get("answer") == r)
        if correct:
            score += 1
        feedback.append({
            "question": q.get("question"),
            "your_answer": r,
            "correct_answer": q.get("answer"),
            "is_correct": correct
        })
    return {"score": score, "total": len(quiz), "feedback": feedback}
