import yfinance as yf

def get_ticker_data(ticker_symbol: str) -> dict:
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        volume = info.get("volume")
        previous_close = info.get("previousClose")
        open_price = info.get("open")
        day_low = info.get("dayLow")
        day_high = info.get("dayHigh")

        hist = ticker.history(period="14d")
        rsi = calculate_rsi(hist["Close"]) if not info.get("rsi") else info.get("rsi")

        return {
            "Ticker": ticker_symbol.upper(),
            "Value": current_price,
            "Previous Close": previous_close,
            "Open": open_price,
            "Day Low": day_low,
            "Day High": day_high,
            "Volume": volume,
            "RSI": rsi
        }

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker_symbol}: {str(e)}"}


def calculate_rsi(series, period: int = 14):
    """Simple RSI calculation from close prices."""
    delta = series.diff().dropna()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2) if not rsi.empty else None