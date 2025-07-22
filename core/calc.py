import pandas as pd


def calculate_rsi(series: pd.Series, period: int = 14) -> float | None:
    """Calculate RSI from a pandas Series of close prices."""
    delta = series.diff().dropna()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2) if not rsi.empty else None


def calculate_ma(series: pd.Series, window: int) -> float | None:
    """Calculate moving average for the given window size."""
    ma = series.rolling(window=window).mean()
    return round(ma.iloc[-1], 2) if not ma.empty else None


def calculate_macd(
    series: pd.Series,
    short_window: int = 12,
    long_window: int = 26,
    signal_window: int = 9,
) -> tuple[float | None, float | None]:
    """Calculate MACD and signal line."""
    exp1 = series.ewm(span=short_window, adjust=False).mean()
    exp2 = series.ewm(span=long_window, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    if macd.empty or signal.empty:
        return None, None
    return round(macd.iloc[-1], 2), round(signal.iloc[-1], 2)


def summarize_option_chain(
    ticker_symbol: str,
) -> dict:
    """Return a summary of the option chain for ``ticker_symbol``.

    Aggregates open interest, volume and implied volatility across all
    expiration dates and calculates Put/Call ratios.
    """
    import yfinance as yf

    symbol = ticker_symbol.upper()
    try:
        ticker = yf.Ticker(symbol)
        expirations = getattr(ticker, "options", [])

        total_call_oi = 0
        total_put_oi = 0
        total_call_vol = 0
        total_put_vol = 0
        call_iv = []
        put_iv = []

        for date in expirations:
            try:
                chain = ticker.option_chain(date)
            except Exception:
                continue

            calls = chain.calls
            puts = chain.puts
            total_call_oi += calls["openInterest"].fillna(0).sum()
            total_put_oi += puts["openInterest"].fillna(0).sum()
            total_call_vol += calls["volume"].fillna(0).sum()
            total_put_vol += puts["volume"].fillna(0).sum()
            call_iv.extend(calls["impliedVolatility"].dropna().tolist())
            put_iv.extend(puts["impliedVolatility"].dropna().tolist())

        def _avg(values: list[float]):
            return sum(values) / len(values) if values else None

        avg_call_iv = _avg(call_iv)
        avg_put_iv = _avg(put_iv)
        avg_iv = _avg(call_iv + put_iv)
        pcr_oi = (total_put_oi / total_call_oi) if total_call_oi else None
        pcr_vol = (total_put_vol / total_call_vol) if total_call_vol else None

        def _round(val):
            return round(val, 4) if val is not None else None

        return {
            "call_open_interest": int(total_call_oi),
            "put_open_interest": int(total_put_oi),
            "call_volume": int(total_call_vol),
            "put_volume": int(total_put_vol),
            "avg_call_iv": _round(avg_call_iv),
            "avg_put_iv": _round(avg_put_iv),
            "avg_iv": _round(avg_iv),
            "pcr_oi": _round(pcr_oi),
            "pcr_vol": _round(pcr_vol),
        }
    except Exception as e:
        return {"error": f"Failed to retrieve options for {symbol}: {e}"}
