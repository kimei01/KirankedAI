from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.models import Question
from claude import claude

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/ask")
async def ask(body: Question):
    user_input = body.question
    answer = claude(user_input)
    return {"answer": answer}
