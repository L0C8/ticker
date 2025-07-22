import yfinance as yf
from core.calc import calculate_rsi, calculate_ma, calculate_macd

try:
    import vectorbt as vbt
except Exception:
    vbt = None

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

        bt_results = run_backtests(close)
        if bt_results:
            data["Backtests"] = bt_results

        return data

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker_symbol}: {str(e)}"}



def run_backtests(close):
    """Run simple backtest strategies using vectorbt if available."""
    if vbt is None:
        return None

    try:
        results = {}

        fast_ma = close.rolling(20).mean()
        slow_ma = close.rolling(50).mean()
        entries = (fast_ma.shift(1) < slow_ma.shift(1)) & (fast_ma >= slow_ma)
        exits = (fast_ma.shift(1) > slow_ma.shift(1)) & (fast_ma <= slow_ma)
        pf_ma = vbt.Portfolio.from_signals(close, entries, exits)
        results["MA20/MA50 Return"] = round(float(pf_ma.total_return()), 4)

        rsi_ind = vbt.RSI.run(close)
        rsi = rsi_ind.rsi
        entries_rsi = (rsi.shift(1) < 30) & (rsi >= 30)
        exits_rsi = (rsi.shift(1) > 70) & (rsi <= 70)
        pf_rsi = vbt.Portfolio.from_signals(close, entries_rsi, exits_rsi)
        results["RSI Return"] = round(float(pf_rsi.total_return()), 4)

        return results
    except Exception:
        return None


