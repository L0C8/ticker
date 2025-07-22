import yfinance as yf
import requests

def get_ticker_data(ticker_symbol: str, api_key: str | None = None) -> dict:
    ticker_symbol = ticker_symbol.upper()
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        if not info:
            return {"error": f"Error: [{ticker_symbol}] not found"}

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        volume = info.get("volume")
        previous_close = info.get("previousClose")
        open_price = info.get("open")
        day_low = info.get("dayLow")
        day_high = info.get("dayHigh")

        hist = ticker.history(period="1y")
        if hist.empty:
            return {"error": f"Error: [{ticker_symbol}] not found"}
        close = hist["Close"]
        rsi = calculate_rsi(close)
        ma20 = calculate_ma(close, 20)
        ma50 = calculate_ma(close, 50)
        ma200 = calculate_ma(close, 200)
        macd_val, macd_signal = calculate_macd(close)

        data = {
            "Ticker": ticker_symbol,
            "Value": current_price,
            "Previous Close": previous_close,
            "Open": open_price,
            "Day Low": day_low,
            "Day High": day_high,
            "Volume": volume,
            "RSI": rsi,
            "MA20": ma20,
            "MA50": ma50,
            "MA200": ma200,
            "MACD": macd_val,
            "MACD Signal": macd_signal,
        }

        if api_key:
            fh = fetch_finnhub_quote(ticker_symbol, api_key)
            if fh:
                data["Finnhub"] = fh

        return data

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


def calculate_ma(series, window: int):
    ma = series.rolling(window=window).mean()
    return round(ma.iloc[-1], 2) if not ma.empty else None


def calculate_macd(series, short_window: int = 12, long_window: int = 26, signal_window: int = 9):
    exp1 = series.ewm(span=short_window, adjust=False).mean()
    exp2 = series.ewm(span=long_window, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    if macd.empty or signal.empty:
        return None, None
    return round(macd.iloc[-1], 2), round(signal.iloc[-1], 2)


def fetch_finnhub_quote(symbol: str, api_key: str) -> dict | None:
    url = "https://finnhub.io/api/v1/quote"
    try:
        resp = requests.get(url, params={"symbol": symbol, "token": api_key}, timeout=5)
        if resp.status_code == 200:
            q = resp.json()
            return {
                "Current": q.get("c"),
                "High": q.get("h"),
                "Low": q.get("l"),
                "Open": q.get("o"),
                "Prev Close": q.get("pc"),
            }
    except Exception:
        pass
    return None
