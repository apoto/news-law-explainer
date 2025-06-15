from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

from gemini_service import GeminiService
from firestore_service import FirestoreService

# 環境変数の読み込み
load_dotenv()

app = FastAPI(title="News Law Explainer API")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# サービスの初期化
gemini_service = GeminiService()
firestore_service = FirestoreService()

class NewsArticle(BaseModel):
    title: str
    content: str

class ArticleResponse(BaseModel):
    id: str
    title: str
    summary: str
    analysis: str
    relatedLaws: List[dict]
    relatedCases: List[dict]
    createdAt: datetime

@app.post("/generate-article", response_model=ArticleResponse)
async def generate_article(article: NewsArticle):
    try:
        # Gemini APIを使用して記事を分析
        analysis_result = await gemini_service.analyze_article(article.content)
        
        # 分析結果をFirestoreに保存
        article_id = await firestore_service.save_article(
            title=article.title,
            summary=analysis_result["summary"],
            analysis=analysis_result["analysis"],
            related_laws=analysis_result["related_laws"],
            related_cases=analysis_result["related_cases"]
        )
        
        # 保存した記事を取得して返す
        saved_article = await firestore_service.get_article(article_id)
        return saved_article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/articles", response_model=List[ArticleResponse])
async def get_articles():
    try:
        articles = await firestore_service.get_articles()
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: str):
    try:
        article = await firestore_service.get_article(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080"))) 