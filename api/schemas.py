from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question : str

class ClaimResult(BaseModel):
    claim : str
    status : str

class AnswerResponse(BaseModel):
    question : str
    chunk_size : int
    top_k : int
    answer : str
    claims : list[ClaimResult]