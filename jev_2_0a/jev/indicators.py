from __future__ import annotations

import pandas as pd


def calculate_sma(close: pd.Series, period: int) -> float | None:
    if len(close) < period:
        return None
    return float(close.rolling(period).mean().iloc[-1])


def calculate_rsi(close: pd.Series, period: int = 14) -> float | None:
    if len(close) < period + 1:
        return None
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    value = rsi.iloc[-1]
    return None if pd.isna(value) else float(value)


def calculate_macd(close: pd.Series) -> dict:
    if len(close) < 35:
        return {"macd": None, "signal": None, "histogram": None}

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    return {
        "macd": float(macd.iloc[-1]),
        "signal": float(signal.iloc[-1]),
        "histogram": float((macd - signal).iloc[-1]),
    }


def calculate_volume_ratio(volume: pd.Series, period: int = 20) -> float | None:
    if len(volume) < period + 1:
        return None
    avg_volume = volume.iloc[-period-1:-1].mean()
    if avg_volume == 0:
        return None
    return float(volume.iloc[-1] / avg_volume)


def calculate_returns(close: pd.Series) -> dict:
    if len(close) < 2:
        return {"1m": None, "3m": None, "6m": None, "1y": None}

    periods = {"1m": 21, "3m": 63, "6m": 126, "1y": 252}
    result = {}

    for name, periods_back in periods.items():
        index = min(periods_back, len(close) - 1)
        result[name] = float(close.iloc[-1] / close.iloc[-index - 1] - 1)

    return result


def calculate_volatility(close: pd.Series, annualization: int = 252) -> float | None:
    returns = close.pct_change().dropna()
    if len(returns) < 20:
        return None
    return float(returns.std() * (annualization ** 0.5))


def calculate_52w_range(close: pd.Series) -> dict:
    if close.empty:
        return {"high": None, "low": None}

    window = close.tail(min(252, len(close)))
    return {
        "high": float(window.max()),
        "low": float(window.min()),
    }
