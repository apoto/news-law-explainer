from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel
import os

class GeminiService:
    def __init__(self):
        # Vertex AIの初期化
        aiplatform.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "asia-northeast1")
        )
        self.model = GenerativeModel("gemini-pro")

    async def analyze_article(self, content: str) -> dict:
        """
        ニュース記事を分析し、要約、法的解説、関連法令、関連判例を抽出する
        """
        prompt = f"""
        以下のニュース記事を分析し、以下の形式で出力してください：

        1. 要約：記事の要点を簡潔にまとめてください。
        2. 法的解説：このニュースに関連する法的な観点からの解説を、専門用語を避けてわかりやすく説明してください。
        3. 関連法令：関連する法令名と条文番号を列挙してください。
        4. 関連判例：関連する重要な判例があれば、その名称と簡単な説明を記載してください。

        ニュース記事：
        {content}
        """

        response = await self.model.generate_content_async(prompt)
        result = response.text

        # レスポンスを解析して構造化データに変換
        # 注：実際の実装では、より堅牢なパース処理が必要
        sections = result.split("\n\n")
        
        return {
            "summary": sections[0].replace("要約：", "").strip(),
            "analysis": sections[1].replace("法的解説：", "").strip(),
            "related_laws": self._parse_laws(sections[2].replace("関連法令：", "").strip()),
            "related_cases": self._parse_cases(sections[3].replace("関連判例：", "").strip())
        }

    def _parse_laws(self, laws_text: str) -> list:
        """
        法令テキストをパースして構造化データに変換
        """
        laws = []
        for law in laws_text.split("\n"):
            if law.strip():
                # 法令名と条文番号を分離
                parts = law.split("第")
                if len(parts) == 2:
                    name = parts[0].strip()
                    article = f"第{parts[1].strip()}"
                    laws.append({
                        "name": name,
                        "article": article,
                        "url": f"https://elaws.e-gov.go.jp/document?lawid={name}"  # 仮のURL
                    })
        return laws

    def _parse_cases(self, cases_text: str) -> list:
        """
        判例テキストをパースして構造化データに変換
        """
        cases = []
        for case in cases_text.split("\n"):
            if case.strip():
                # 判例名と説明を分離
                parts = case.split("：")
                if len(parts) == 2:
                    name = parts[0].strip()
                    summary = parts[1].strip()
                    cases.append({
                        "name": name,
                        "summary": summary,
                        "url": f"https://www.courts.go.jp/app/hanrei_jp/list1?filter=1&keyword={name}"  # 仮のURL
                    })
        return cases 