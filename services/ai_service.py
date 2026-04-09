import os
import json
from groq import Groq

client = None

def get_groq_client():
    global client
    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("Warning: GROQ_API_KEY not set. Using fallback analysis.")
            client = None  # Will use fallback
            return None
        client = Groq(api_key=api_key)
    return client

def analyze_with_groq(stock_data: dict, news: list) -> dict:
    """Send stock data + news to Groq LLM and get AI analysis."""

    news_text = "\n".join([
        f"- {n['title']}: {n.get('description', '')}"
        for n in news
    ])

    stock_text = f"""
Symbol: {stock_data['symbol']}
Name: {stock_data['name']}
Current Price: {stock_data['current_price']}
Previous Close: {stock_data['previous_close']}
Day High: {stock_data['day_high']}
Day Low: {stock_data['day_low']}
Volume: {stock_data['volume']}
PE Ratio: {stock_data['pe_ratio']}
52-Week High: {stock_data['52_week_high']}
52-Week Low: {stock_data['52_week_low']}
    """.strip()

    prompt = f"""
You are a financial AI analyst.

Analyze the following stock data and recent news.

Stock Data:
{stock_text}

News Headlines:
{news_text}

Tasks:
1. Determine the market sentiment (Bullish / Bearish / Neutral)
2. Provide a recommendation (Buy / Hold / Sell)
3. Suggest an entry point (price or condition)
4. Explain reasoning in simple terms
5. Mention risks if any

Output STRICTLY in JSON format only, no extra text:
{{
  "sentiment": "",
  "recommendation": "",
  "entry_point": "",
  "reason": "",
  "risks": ""
}}
    """.strip()

    groq_client = get_groq_client()
    if groq_client is None:
        return {
            "sentiment": "Neutral",
            "recommendation": "Hold",
            "entry_point": "N/A",
            "reason": "GROQ_API_KEY not configured. Please add to .env and restart. Fallback analysis.",
            "risks": "No AI analysis available"
        }

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )

        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except json.JSONDecodeError:
        return {
            "sentiment": "Neutral",
            "recommendation": "Hold",
            "entry_point": "N/A",
            "reason": "Could not parse AI response. Please try again.",
            "risks": "Analysis unavailable"
        }
    except Exception as e:
        return {
            "sentiment": "Error",
            "recommendation": "N/A",
            "entry_point": "N/A",
            "reason": str(e),
            "risks": "API Error"
        }
