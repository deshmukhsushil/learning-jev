from dataclasses import asdict, dataclass
from typing import Any

@dataclass
class StockState:
    symbol: str
    company_name: str | None
    currency: str | None
    price: float | None
    volume: float | None
    sma20: float | None
    sma50: float | None
    sma200: float | None
    rsi14: float | None
    macd: float | None
    macd_signal: float | None
    macd_histogram: float | None
    average_volume_20d: float | None
    volume_ratio: float | None
    return_1m: float | None
    return_3m: float | None
    return_6m: float | None
    return_1y: float | None
    volatility_1y: float | None
    high_52w: float | None
    low_52w: float | None
    distance_from_52w_high: float | None
    distance_from_52w_low: float | None
    pe_ratio: float | None
    peg_ratio: float | None
    price_to_book: float | None
    roe: float | None
    profit_margin: float | None
    operating_margin: float | None
    debt_to_equity: float | None
    revenue_cagr_5y: float | None
    eps_cagr_5y: float | None
    sector: str | None
    industry: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class JEVResult:
    symbol: str
    choices: dict[str, Any]
    scores: dict[str, Any]
    nouls: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"symbol": self.symbol, "choices": self.choices, "scores": self.scores, "nouls": self.nouls}
