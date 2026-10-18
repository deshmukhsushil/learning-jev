from __future__ import annotations
import math
from typing import Any
import pandas as pd
import yfinance as yf
from config import HISTORY_PERIOD, RSI_PERIOD, VOLUME_WINDOW, CAGR_YEARS
from .fundamentals import calculate_cagr
from .indicators import calculate_rsi, calculate_macd, calculate_returns, calculate_volatility
from .models import StockState


def safe_float(value: Any) -> float | None:
    try:
        number = float(value)
        return None if math.isnan(number) or math.isinf(number) else number
    except (TypeError, ValueError):
        return None


def extract_financial_data(df: pd.DataFrame, keys: list[str]) -> list:
    if df.empty:
        return []
    for key in keys:
        if key in df.index:
            return df.loc[key].iloc[::-1].tolist()
    return []


def get_stock_state(symbol: str) -> StockState:
    print(f"Fetching data for {symbol}...")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=HISTORY_PERIOD, auto_adjust=False)

    if hist.empty:
        raise ValueError(f"No price data returned for {symbol}")

    close = hist["Close"].dropna()
    volume = hist["Volume"].dropna()

    if close.empty:
        raise ValueError(f"No closing-price data returned for {symbol}")

    price = safe_float(close.iloc[-1])
    latest_volume = safe_float(volume.iloc[-1]) if not volume.empty else None

    sma20 = safe_float(close.rolling(20).mean().iloc[-1])
    sma50 = safe_float(close.rolling(50).mean().iloc[-1])
    sma200 = safe_float(close.rolling(200).mean().iloc[-1])

    rsi14 = safe_float(calculate_rsi(close, RSI_PERIOD))
    macd_data = calculate_macd(close)

    avg_vol = safe_float(volume.rolling(VOLUME_WINDOW).mean().iloc[-1])
    volume_ratio = latest_volume / avg_vol if latest_volume is not None and avg_vol not in (None, 0) else None

    returns = calculate_returns(close)
    high_52w, low_52w = safe_float(close.max()), safe_float(close.min())
    dist_high = price / high_52w - 1 if price is not None and high_52w else None
    dist_low = price / low_52w - 1 if price is not None and low_52w else None

    try:
        info = ticker.info or {}
    except Exception:
        info = {}

    try:
        income = ticker.income_stmt
    except Exception:
        income = pd.DataFrame()

    rev_values = extract_financial_data(income, ["Total Revenue", "Operating Revenue"])
    eps_values = extract_financial_data(income, ["Diluted EPS", "Basic EPS"])

    return StockState(
        symbol=symbol,
        company_name=info.get("longName") or info.get("shortName"),
        currency=info.get("currency"),
        price=price,
        volume=latest_volume,
        sma20=sma20,
        sma50=sma50,
        sma200=sma200,
        rsi14=rsi14,
        macd=safe_float(macd_data.get("macd")),
        macd_signal=safe_float(macd_data.get("signal")),
        macd_histogram=safe_float(macd_data.get("histogram")),
        average_volume_20d=avg_vol,
        volume_ratio=safe_float(volume_ratio),
        return_1m=returns["1m"],
        return_3m=returns["3m"],
        return_6m=returns["6m"],
        return_1y=returns["1y"],
        volatility_1y=safe_float(calculate_volatility(close)),
        high_52w=high_52w,
        low_52w=low_52w,
        distance_from_52w_high=safe_float(dist_high),
        distance_from_52w_low=safe_float(dist_low),
        pe_ratio=safe_float(info.get("trailingPE")),
        peg_ratio=safe_float(info.get("pegRatio")),
        price_to_book=safe_float(info.get("priceToBook")),
        roe=safe_float(info.get("returnOnEquity")),
        profit_margin=safe_float(info.get("profitMargins")),
        operating_margin=safe_float(info.get("operatingMargins")),
        debt_to_equity=safe_float(info.get("debtToEquity")),
        revenue_cagr_5y=safe_float(calculate_cagr(rev_values, CAGR_YEARS)),
        eps_cagr_5y=safe_float(calculate_cagr(eps_values, CAGR_YEARS)),
        sector=info.get("sector"),
        industry=info.get("industry"),
    )


def fetch_all_states(symbols: list[str]) -> list[StockState]:
    states = []
    for symbol in symbols:
        try:
            states.append(get_stock_state(symbol))
            print(f"Successfully processed: {symbol}")
        except Exception as exc:
            print(f"Failed: {symbol} -> {exc}")
    return states