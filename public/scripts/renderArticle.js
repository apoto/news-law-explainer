// APIのベースURL
const API_BASE_URL = "https://your-cloud-run-url.run.app";

// URLから記事IDを取得する関数
function getArticleId() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

// 記事詳細を取得する関数
async function fetchArticleDetails() {
  const articleId = getArticleId();
  if (!articleId) {
    showError("記事IDが指定されていません。");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/articles/${articleId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const article = await response.json();
    displayArticle(article);
  } catch (error) {
    console.error("記事の取得に失敗しました:", error);
    showError("記事の読み込みに失敗しました。後ほど再度お試しください。");
  }
}

// 記事詳細を表示する関数
function displayArticle(article) {
  const articleContent = document.getElementById("article-content");

  // タイトルを更新
  document.title = `${article.title} - ニュース法解説エージェント`;

  articleContent.innerHTML = `
        <div class="article-detail">
            <h1 class="mdc-typography--headline4">${article.title}</h1>
            <div class="article-meta">
                <span>${new Date(article.createdAt).toLocaleDateString(
                  "ja-JP"
                )}</span>
            </div>
            
            <div class="article-summary mdc-typography--body1">
                <h2 class="mdc-typography--headline6">ニュース要約</h2>
                <p>${article.summary}</p>
            </div>

            <div class="article-analysis mdc-typography--body1">
                <h2 class="mdc-typography--headline6">法的解説</h2>
                <p>${article.analysis}</p>
            </div>

            <div class="article-laws mdc-typography--body1">
                <h2 class="mdc-typography--headline6">関連法令</h2>
                <ul>
                    ${article.relatedLaws
                      .map(
                        (law) => `
                        <li>
                            <a href="${law.url}" target="_blank" rel="noopener noreferrer">
                                ${law.name}
                            </a>
                        </li>
                    `
                      )
                      .join("")}
                </ul>
            </div>

            <div class="article-cases mdc-typography--body1">
                <h2 class="mdc-typography--headline6">関連判例</h2>
                <ul>
                    ${article.relatedCases
                      .map(
                        (case_) => `
                        <li>
                            <a href="${case_.url}" target="_blank" rel="noopener noreferrer">
                                ${case_.name}
                            </a>
                            <p class="case-summary">${case_.summary}</p>
                        </li>
                    `
                      )
                      .join("")}
                </ul>
            </div>
        </div>
    `;
}

// エラーメッセージを表示する関数
function showError(message) {
  const articleContent = document.getElementById("article-content");
  articleContent.innerHTML = `
        <div class="mdc-typography--body1" style="color: #d32f2f; padding: 16px;">
            ${message}
        </div>
    `;
}

// ページ読み込み時に記事詳細を取得
document.addEventListener("DOMContentLoaded", fetchArticleDetails);
