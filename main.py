
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# ✅ 루트 GET 요청 (Render 헬스체크용)
@app.get("/")
async def root():
    return JSONResponse(
        content={"status": "ok", "message": "Perplexity Render 서버 정상 작동 중입니다."},
        media_type="application/json; charset=utf-8"
    )

# ✅ 루트 HEAD 요청 (Render/UptimeRobot에서 발생)
@app.head("/")
async def root_head():
    return JSONResponse(status_code=200)

# ✅ Perplexity API 프록시 POST 요청
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
