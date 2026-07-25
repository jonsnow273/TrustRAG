from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from pipeline import run_pipeline
from api.schemas import QuestionRequest, AnswerResponse

app = FastAPI()


@app.post("/ask", response_model=AnswerResponse)
def answer_question(request: QuestionRequest):
    result = run_pipeline(request.question)
    return result