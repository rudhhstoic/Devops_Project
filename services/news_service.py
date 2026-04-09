import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(symbol: str) -> list:
    """Fetch latest news headlines for a stock symbol."""
    if not NEWS_API_KEY:
        return [{"title": "News API key not configured", "description": ""}]

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        articles = data.get("articles", [])
        return [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "published": a.get("publishedAt", "")
            }
            for a in articles[:5]
        ]
    except Exception as e:
        return [{"title": f"Could not fetch news: {str(e)}", "description": ""}]
