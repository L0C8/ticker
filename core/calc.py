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
