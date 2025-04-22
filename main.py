from fastapi import FastAPI, Request
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

@app.post("/research")
async def research(request: Request):
    data = await request.json()
    question = data.get("query")
    if not question:
        return {"error": "No query provided"}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "pplx-70b-online",
        "messages": [
            {"role": "system", "content": "Answer using real-time data with sources."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()
