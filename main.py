import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.rag import RAG

load_dotenv()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserPrompt(BaseModel):
    prompt: str


api_key = os.getenv("OPENAI_API_KEY")
rag_instance = RAG(api_key)


@app.get("/")
def read_root():
    return {"Hello": "Word"}


@app.post("/generate")
async def generate_result(input: UserPrompt):
    result = rag_instance.generate(input.prompt)

    if result == None:
        return {"status": "failure", "message": "Cannot generate answer."}

    return result
