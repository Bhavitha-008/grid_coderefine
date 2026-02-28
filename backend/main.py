from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class CodeRequest(BaseModel):
    code: str

@app.post("/analyze")
def analyze_code(request: CodeRequest):

    prompt = f"""
You are an AI Code Review and Rewrite Agent.

Analyze the following code carefully:

1. Detect bugs
2. Identify performance issues
3. Identify security vulnerabilities
4. Suggest improvements
5. Provide an optimized rewritten version
6. Give a code quality score out of 100

Code:
{request.code}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()
    analysis_text = result["choices"][0]["message"]["content"]

    return {"analysis": analysis_text}
