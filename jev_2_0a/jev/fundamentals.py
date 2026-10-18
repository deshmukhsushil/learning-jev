from __future__ import annotations


def get_number(value):
    if value in (None, "", "None", "N/A"):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def calculate_cagr(values, target_years: int = 5):
    cleaned = []
    for value in values:
        try:
            value = float(value)
        except (TypeError, ValueError):
            continue
        if value > 0:
            cleaned.append(value)

    if len(cleaned) < 2:
        return None

    observed_years = min(target_years, len(cleaned) - 1)
    start = cleaned[-(observed_years + 1)]
    end = cleaned[-1]

    if start <= 0 or end <= 0:
        return None

    return float((end / start) ** (1 / observed_years) - 1)
