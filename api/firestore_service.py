from google.cloud import firestore
from datetime import datetime
import os

class FirestoreService:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("articles")

    async def save_article(self, title: str, summary: str, analysis: str, 
                         related_laws: list, related_cases: list) -> str:
        """
        記事をFirestoreに保存する
        """
        article_data = {
            "title": title,
            "summary": summary,
            "analysis": analysis,
            "relatedLaws": related_laws,
            "relatedCases": related_cases,
            "createdAt": datetime.utcnow()
        }

        # ドキュメントを追加
        doc_ref = self.collection.add(article_data)
        return doc_ref[1].id

    async def get_article(self, article_id: str) -> dict:
        """
        特定の記事を取得する
        """
        doc_ref = self.collection.document(article_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        data["id"] = doc.id
        return data

    async def get_articles(self) -> list:
        """
        全ての記事を取得する（作成日時の降順）
        """
        articles = []
        docs = self.collection.order_by("createdAt", direction=firestore.Query.DESCENDING).stream()

        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            articles.append(data)

        return articles 