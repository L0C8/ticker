import yfinance as yf
from core.calc import (
    calculate_rsi,
    calculate_ma,
    calculate_macd,
    summarize_option_chain,
    random_forest_prediction,
    xgboost_prediction,
)

def get_ticker_data(ticker_symbol: str) -> dict:
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

        # fetch market context
        spy = yf.Ticker("SPY").history(period="1y")["Close"]
        uup = yf.Ticker("UUP").history(period="1y")["Close"]

        rsi = calculate_rsi(close)
        spy_rsi = calculate_rsi(spy)
        uup_rsi = calculate_rsi(uup)
        rel_strength = round(close.iloc[-1] / spy.iloc[-1], 4) if not spy.empty else None

        ma20 = calculate_ma(close, 20)
        ma50 = calculate_ma(close, 50)
        ma200 = calculate_ma(close, 200)
        macd_val, macd_signal = calculate_macd(close)
        rf_pred = random_forest_prediction(close, spy=spy, uup=uup)
        xgb_pred = xgboost_prediction(close, spy=spy, uup=uup)

        options_summary = summarize_option_chain(ticker_symbol)

        data = {
            "Ticker": ticker_symbol,
            "Value": current_price,
            "Previous Close": previous_close,
            "Open": open_price,
            "Day Low": day_low,
            "Day High": day_high,
            "Volume": volume,
            "RSI": rsi,
            "SPY RSI": spy_rsi,
            "UUP RSI": uup_rsi,
            "Relative Strength": rel_strength,
            "MA20": ma20,
            "MA50": ma50,
            "MA200": ma200,
            "MACD": macd_val,
            "MACD Signal": macd_signal,
            "Random Forest Prediction": rf_pred,
            "XGBoost Prediction": xgb_pred,
            "Options": options_summary,
        }

        return data

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker_symbol}: {str(e)}"}


