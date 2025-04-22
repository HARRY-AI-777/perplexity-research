
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse  # ✅ 이 줄 추가
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# ✅ Render 헬스체크용 루트 경로 추가
@app.get("/")
def root():
    return {"status": "ok", "message": "Perplexity Render 서버 정상 작동 중입니다."}
# ✅ 이 부분을 추가!
@app.head("/")
async def root_head():
    return JSONResponse(status_code=200)
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
