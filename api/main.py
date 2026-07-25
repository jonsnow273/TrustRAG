from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from pipeline import run_pipeline
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import QuestionRequest, AnswerResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask", response_model=AnswerResponse)
def answer_question(request: QuestionRequest):
    result = run_pipeline(request.question)
    return result