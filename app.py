from flask import Flask, render_template, jsonify, request
from services.stock_service import get_stock_data
from services.news_service import get_news
from services.ai_service import analyze_with_groq
from services.email_service import send_email
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# In-memory watchlist (replace with DB for production)
watchlist = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/watchlist", methods=["GET"])
def get_watchlist():
    return jsonify(watchlist)

@app.route("/api/watchlist", methods=["POST"])
def add_stock():
    data = request.get_json()
    symbol = data.get("symbol", "").upper().strip()
    email = data.get("email", "")
    if symbol and symbol not in [s["symbol"] for s in watchlist]:
        watchlist.append({"symbol": symbol, "email": email})
    return jsonify({"message": f"{symbol} added to watchlist"})

@app.route("/api/watchlist/<symbol>", methods=["DELETE"])
def remove_stock(symbol):
    global watchlist
    watchlist = [s for s in watchlist if s["symbol"] != symbol.upper()]
    return jsonify({"message": f"{symbol} removed"})

@app.route("/api/analyze/<symbol>")
def analyze(symbol):
    symbol = symbol.upper()
    try:
        stock_data = get_stock_data(symbol)
        news = get_news(symbol)
        ai_result = analyze_with_groq(stock_data, news)

        # Try to send email if user email is known
        user_email = next(
            (s.get("email") for s in watchlist if s["symbol"] == symbol), None
        )
        if user_email and user_email != "":
            try:
                send_email(user_email, symbol, ai_result)
            except Exception as e:
                print(f"Email failed: {e}")

        return jsonify({
            "symbol": symbol,
            "stock": stock_data,
            "analysis": ai_result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
