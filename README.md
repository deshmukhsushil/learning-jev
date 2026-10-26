# JEV Powered Quant Research Engine

## Diagram

<img width="4507" height="5344" alt="image" src="https://github.com/user-attachments/assets/876b5ac9-af4e-4957-a35c-a75c0d2f2867" />


## Included
- 1-year Yahoo Finance history
- SMA20 / SMA50 / SMA200
- RSI14
- MACD, signal and histogram
- 20-day average volume and volume ratio
- 1m / 3m / 6m / 1y returns
- annualized volatility
- 52-week high/low and distance from them
- P/E, PEG, P/B, ROE, margins, debt/equity
- revenue/EPS CAGR when usable annual data is available
- metric-by-metric peer percentiles
- structured JEV output
- optional JSON export

## Setup

Python 3.11+ recommended.

```bash
python -m venv .venv
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your TypeSafe credential there. If your installed SDK expects a different environment variable, adjust `jev/ai.py` according to its SDK documentation.

Run:

```bash
python main.py
python main.py --stocks BEL.NS BHEL.NS HDFCBANK.NS ONGC.NS
python main.py --output data/jev_report.json
```

## Architecture

```text
Yahoo Finance
      ↓
historical prices + company fundamentals
      ↓
feature calculation
      ↓
validated StockState
      ↓
JEV structured analysis
      ↓
metric-by-metric peer context
      ↓
terminal report / JSON
```

## Important caveats

Yahoo Finance data can be missing or inconsistent. CAGR calculations use available annual observations and return `None` when a meaningful positive-start CAGR cannot be calculated. This is a research prototype, not a trading or investment recommendation system.

The JEV bullish setup value is deliberately described as an assessment of the supplied evidence rather than a literal probability of future returns. The next major version should backtest and calibrate these signals before assigning probabilistic meaning to them.
