from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.models import Question
from claude import add_user_message, process_chat

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/ask")
async def ask(body: Question):
    user_input = body.question
    add_user_message(body.history, user_input)
    #If the conversation history exceeds 20 messages, keep only the last 20 to stay within context limits. 
    if len(body.history) > 20:
        body.history = body.history[-20:]
        #Checks if messages contains any text at all and if the first message is a tool result
        while body.history and body.history[0]['content'][0]['type'] == "tool_result":
                body.history = body.history[1:]
    answer = process_chat(body.question, body.history)
    return answer
