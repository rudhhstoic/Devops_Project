# 🤖 AI Stock Advisor

An AI-powered stock analysis system using real-time data, news sentiment, and Groq LLM — deployed with DevOps best practices.

## System Architecture

```
User → Frontend (HTML) → Flask Backend → yfinance + NewsAPI → Groq LLM → Dashboard + Email Alert
```

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Flask (Python) |
| Stock Data | yfinance |
| News Data | NewsAPI |
| AI Engine | Groq (LLaMA3) |
| Frontend | HTML + Chart.js |
| Email | Gmail SMTP |
| DevOps | Git, Docker, Railway, GitHub Actions |

## Setup Instructions

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd ai-stock-advisor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Get your keys from:
- **Groq API**: https://console.groq.com
- **NewsAPI**: https://newsapi.org
- **Gmail**: Use App Password from Google Account → Security → App Passwords

### 3. Run Locally
```bash
python app.py
# Visit http://localhost:5000
```

### 4. Docker
```bash
docker build -t ai-stock-advisor .
docker run -p 5000:5000 --env-file .env ai-stock-advisor
```

### 5. Deploy on Railway
1. Push code to GitHub
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Add environment variables (GROQ_API_KEY, NEWS_API_KEY, EMAIL, EMAIL_PASSWORD)
4. Deploy!

## Stock Symbol Examples

| Stock | Symbol |
|-------|--------|
| TCS | TCS.NS |
| Reliance | RELIANCE.NS |
| Infosys | INFY.NS |
| Apple | AAPL |
| Tesla | TSLA |
| Google | GOOGL |

## Features

- Real-time stock data via Yahoo Finance
- Latest news headlines per stock
- AI sentiment analysis (Bullish/Bearish/Neutral)
- Buy / Hold / Sell recommendations
- Email alerts on analysis
- 5-day price trend chart
- CI/CD via GitHub Actions
- Docker support

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Dashboard UI |
| GET | /api/watchlist | Get all watched stocks |
| POST | /api/watchlist | Add stock to watchlist |
| DELETE | /api/watchlist/\<symbol\> | Remove stock |
| GET | /api/analyze/\<symbol\> | Run AI analysis |
