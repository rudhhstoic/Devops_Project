import yfinance as yf

def get_stock_data(symbol: str) -> dict:
    """Fetch real-time stock data using yfinance."""
    ticker = yf.Ticker(symbol)
    info = ticker.info

    hist = ticker.history(period="5d")
    prices = hist["Close"].tolist()
    dates = [str(d.date()) for d in hist.index]

    return {
        "symbol": symbol,
        "name": info.get("longName", symbol),
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
        "previous_close": info.get("previousClose", 0),
        "open": info.get("open", 0),
        "day_high": info.get("dayHigh", 0),
        "day_low": info.get("dayLow", 0),
        "volume": info.get("volume", 0),
        "market_cap": info.get("marketCap", 0),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", 0),
        "52_week_low": info.get("fiftyTwoWeekLow", 0),
        "price_history": {"dates": dates, "prices": prices}
    }
