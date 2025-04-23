from fastapi import FastAPI
from pydantic import BaseModel
import threading
import time
import requests

app = FastAPI()

# Perplexity용 요청 포맷
class Query(BaseModel):
    query: str
    lang: str = "ko"

# POST /research → Perplexity 응답 시뮬레이션
@app.post("/research")
def research(query: Query):
    return {
        "result": f"Perplexity 응답 시뮬레이션: {query.query} (언어: {query.lang})"
    }

# GET / → UptimeRobot 헬스체크용
@app.get("/")
def root():
    return {
        "status": "Replit 서버는 정상 작동 중입니다."
    }

# Keep-Alive 루프 → Replit 절전 방지
def keep_alive():
    while True:
        try:
            requests.get("https://perplexity-research-server.webtools21.replit.app/")
        except:
            pass
        time.sleep(300)  # 5분 간격

# 루프 실행
threading.Thread(target=keep_alive, daemon=True).start()
