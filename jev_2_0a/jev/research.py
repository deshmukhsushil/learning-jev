from __future__ import annotations
from typing import Any
from .models import StockState

def rank_peer_percentile(states: list[StockState], field: str, higher_is_better: bool = True) -> dict[str, float | None]:
    values = [(s.symbol, float(getattr(s, field))) for s in states if getattr(s, field) is not None]
    result = {s.symbol: None for s in states}
    if not values: return result
    ordered = sorted(values, key=lambda x: x[1])
    n = len(ordered)
    for pos, (symbol, _) in enumerate(ordered):
        percentile = 50.0 if n == 1 else 100 * pos / (n - 1)
        result[symbol] = percentile if higher_is_better else 100 - percentile
    return result

def build_peer_context(states: list[StockState]) -> dict[str, dict[str, Any]]:
    fields = {"return_1y":True,"roe":True,"revenue_cagr_5y":True,"eps_cagr_5y":True,"pe_ratio":False,"price_to_book":False,"volatility_1y":False}
    context = {s.symbol:{} for s in states}
    for field, higher_is_better in fields.items():
        for symbol, percentile in rank_peer_percentile(states, field, higher_is_better).items():
            context[symbol][f"{field}_peer_percentile"] = percentile
    return context
