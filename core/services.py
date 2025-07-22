import yfinance as yf
import requests
from core.calc import calculate_rsi, calculate_ma, calculate_macd

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
            quote = fetch_finnhub_quote(ticker_symbol, api_key)
            profile = fetch_finnhub_profile(ticker_symbol, api_key)
            if quote:
                if "error" in quote:
                    data["Finnhub"] = quote
                else:
                    data["Finnhub Quote"] = quote
            if profile:
                if "error" in profile:
                    data["Finnhub"] = profile
                else:
                    data["Finnhub Profile"] = profile

        return data

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker_symbol}: {str(e)}"}



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
        if resp.status_code in (401, 403):
            return {"error": "invalid key"}
    except Exception:
        pass
    return None


def fetch_finnhub_profile(symbol: str, api_key: str) -> dict | None:
    url = "https://finnhub.io/api/v1/stock/profile2"
    try:
        resp = requests.get(url, params={"symbol": symbol, "token": api_key}, timeout=5)
        if resp.status_code == 200:
            p = resp.json()
            return {
                "Name": p.get("name"),
                "Exchange": p.get("exchange"),
                "Industry": p.get("finnhubIndustry"),
                "MarketCap": p.get("marketCapitalization"),
            }
        if resp.status_code in (401, 403):
            return {"error": "invalid key"}
    except Exception:
        pass
    return None
