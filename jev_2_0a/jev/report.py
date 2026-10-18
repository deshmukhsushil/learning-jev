from __future__ import annotations


def fmt(value, percent=False, decimals=2):
    if value is None:
        return "N/A"
    if percent:
        return f"{value * 100:.{decimals}f}%"
    return f"{value:.{decimals}f}"


def pctile(value):
    if value is None:
        return "N/A"
    return f"{value:.0f}"


def choice_value(obj):
    return obj.get("choice", "N/A") if isinstance(obj, dict) else "N/A"


def confidence_value(obj):
    if not isinstance(obj, dict):
        return "N/A"
    value = obj.get("confidence")
    return "N/A" if value is None else f"{value:.2f}"


def score_value(obj):
    if not isinstance(obj, dict):
        return "N/A"
    value = obj.get("score")
    return "N/A" if value is None else f"{value:.2f}/4"


def noul_value(obj):
    if not isinstance(obj, dict):
        return "N/A"
    value = obj.get("noul")
    return "N/A" if value is None else f"{value:.2f}"


def probability(obj, key):
    if not isinstance(obj, dict):
        return "N/A"
    probs = obj.get("probabilities", {})
    value = probs.get(key)
    return "N/A" if value is None else f"{value * 100:.0f}%"


def print_table(title, headers, rows):
    print("\n" + "-" * 120)
    print(title)
    print("-" * 120)

    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    header = " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    divider = "-+-".join("-" * widths[i] for i in range(len(headers)))

    print(header)
    print(divider)
    for row in rows:
        print(" | ".join(str(value).ljust(widths[i]) for i, value in enumerate(row)))


def print_report(states, results, peer_context=None):
    if peer_context is None:
        peer_context = {}

    print("\n" + "=" * 120)
    print("JEV 2.0A - QUANT RESEARCH ENGINE")
    print("=" * 120)

    market_rows = []
    for state in states:
        market_rows.append([
            state.symbol,
            fmt(state.price),
            fmt(state.sma20),
            fmt(state.sma50),
            fmt(state.sma200),
            fmt(state.rsi14),
            fmt(state.macd),
            fmt(state.macd_signal),
            fmt(state.macd_histogram),
            fmt(state.volume_ratio),
            fmt(state.return_1m, True),
            fmt(state.return_3m, True),
            fmt(state.return_6m, True),
            fmt(state.return_1y, True),
            fmt(state.volatility_1y, True),
            fmt(state.high_52w),
            fmt(state.low_52w),
        ])

    print_table(
        "MARKET & TECHNICALS",
        [
            "Stock", "Price", "SMA20", "SMA50", "SMA200", "RSI",
            "MACD", "Signal", "Hist", "Vol Ratio",
            "1M", "3M", "6M", "1Y", "Volatility", "52W High", "52W Low"
        ],
        market_rows,
    )

    fund_rows = []
    for state in states:
        fund_rows.append([
            state.symbol,
            fmt(state.pe_ratio),
            fmt(state.peg_ratio),
            fmt(state.price_to_book),
            fmt(state.roe, True),
            fmt(state.profit_margin, True),
            fmt(state.operating_margin, True),
            fmt(state.debt_to_equity),
            fmt(state.revenue_cagr_5y, True),
            fmt(state.eps_cagr_5y, True),
        ])

    print_table(
        "FUNDAMENTALS",
        [
            "Stock", "P/E", "PEG", "P/B", "ROE", "Profit Margin",
            "Operating Margin", "Debt/Equity", "Revenue CAGR*", "EPS CAGR*"
        ],
        fund_rows,
    )

    analysis_rows = []
    for result in results:
        trend = result.choices["technical_trend"]
        strength = result.scores["technical_strength"]
        bullish = result.nouls["bullish_setup"]
        valuation = result.choices["valuation"]
        growth = result.choices["growth_profile"]

        analysis_rows.append([
            result.symbol,
            choice_value(trend),
            confidence_value(trend),
            score_value(strength),
            noul_value(bullish),
            choice_value(valuation),
            confidence_value(valuation),
            choice_value(growth),
            confidence_value(growth),
        ])

    print_table(
        "JEV ANALYSIS",
        [
            "Stock", "Technical Trend", "Trend Conf.", "Technical Strength",
            "Bullish Setup", "Valuation", "Val. Conf.", "Growth", "Growth Conf."
        ],
        analysis_rows,
    )

    probability_rows = []
    for result in results:
        trend = result.choices["technical_trend"]
        valuation = result.choices["valuation"]
        growth = result.choices["growth_profile"]

        probability_rows.append([
            result.symbol,
            probability(trend, "bullish"),
            probability(trend, "neutral"),
            probability(trend, "bearish"),
            probability(valuation, "attractive"),
            probability(valuation, "reasonable"),
            probability(valuation, "expensive"),
            probability(growth, "strong"),
            probability(growth, "moderate"),
            probability(growth, "weak"),
        ])

    print_table(
        "JEV PROBABILITY DISTRIBUTIONS",
        [
            "Stock", "Tech Bull", "Tech Neutral", "Tech Bear",
            "Val Attractive", "Val Reasonable", "Val Expensive",
            "Growth Strong", "Growth Moderate", "Growth Weak"
        ],
        probability_rows,
    )

    peer_rows = []
    for result in results:
        peer = peer_context.get(result.symbol, {})
        peer_rows.append([
            result.symbol,
            pctile(peer.get("return_1y_peer_percentile")),
            pctile(peer.get("roe_peer_percentile")),
            pctile(peer.get("revenue_cagr_5y_peer_percentile")),
            pctile(peer.get("eps_cagr_5y_peer_percentile")),
            pctile(peer.get("pe_ratio_peer_percentile")),
            pctile(peer.get("price_to_book_peer_percentile")),
            pctile(peer.get("volatility_1y_peer_percentile")),
        ])

    print_table(
        "PEER CONTEXT - METRIC-BY-METRIC PERCENTILES",
        [
            "Stock", "1Y Return", "ROE", "Revenue CAGR", "EPS CAGR",
            "P/E", "P/B", "Volatility"
        ],
        peer_rows,
    )

    quality_rows = []
    for state in states:
        missing = []
        fields = [
            ("SMA20", state.sma20),
            ("SMA50", state.sma50),
            ("SMA200", state.sma200),
            ("RSI14", state.rsi14),
            ("MACD", state.macd),
            ("1Y Return", state.return_1y),
            ("ROE", state.roe),
            ("Revenue CAGR", state.revenue_cagr_5y),
            ("EPS CAGR", state.eps_cagr_5y),
        ]
        for name, value in fields:
            if value is None:
                missing.append(name)

        quality_rows.append([
            state.symbol,
            "OK" if not missing else "PARTIAL",
            ", ".join(missing) if missing else "None",
        ])

    print_table(
        "DATA QUALITY / AVAILABILITY",
        ["Stock", "Status", "Missing / Unavailable Fields"],
        quality_rows,
    )

    print("\nNotes:")
    print("* CAGR is based on annual observations available from Yahoo Finance, up to the five-year target.")
    print("* Peer percentiles are metric-by-metric context, not an overall stock ranking.")
    print("* JEV bullish_setup is a model assessment of supplied evidence, not a literal return probability.")
    print("* ROE and other provider-derived fundamentals are unavailable for some companies.")
    print("* Debt/Equity requires validation against statement-level definitions before using it for serious research.")