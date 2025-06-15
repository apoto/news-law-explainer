// APIのベースURL
const API_BASE_URL = "https://your-cloud-run-url.run.app";

// 記事一覧を取得する関数
async function fetchArticles() {
  try {
    const response = await fetch(`${API_BASE_URL}/articles`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const articles = await response.json();
    displayArticles(articles);
  } catch (error) {
    console.error("記事の取得に失敗しました:", error);
    showError("記事の読み込みに失敗しました。後ほど再度お試しください。");
  }
}

// 記事一覧を表示する関数
function displayArticles(articles) {
  const articlesList = document.getElementById("articles-list");
  articlesList.innerHTML = "";

  if (articles.length === 0) {
    articlesList.innerHTML = `
            <div class="mdc-typography--body1" style="padding: 16px;">
                記事がまだありません。
            </div>
        `;
    return;
  }

  articles.forEach((article) => {
    const articleCard = createArticleCard(article);
    articlesList.appendChild(articleCard);
  });
}

// 記事カードを作成する関数
function createArticleCard(article) {
  const card = document.createElement("div");
  card.className = "article-card";
  card.innerHTML = `
        <div class="article-card__content">
            <h2 class="article-card__title">
                <a href="article.html?id=${article.id}">${article.title}</a>
            </h2>
            <p class="article-card__summary">${article.summary}</p>
            <div class="article-card__meta">
                <span>${new Date(article.createdAt).toLocaleDateString(
                  "ja-JP"
                )}</span>
                <span>関連法令: ${article.relatedLaws.join(", ")}</span>
            </div>
        </div>
    `;
  return card;
}

// エラーメッセージを表示する関数
function showError(message) {
  const articlesList = document.getElementById("articles-list");
  articlesList.innerHTML = `
        <div class="mdc-typography--body1" style="color: #d32f2f; padding: 16px;">
            ${message}
        </div>
    `;
}

// ページ読み込み時に記事一覧を取得
document.addEventListener("DOMContentLoaded", fetchArticles);
