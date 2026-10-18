from __future__ import annotations

from dotenv import load_dotenv
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

from .models import JEVResult, StockState

load_dotenv()

client = TypeSafeClient()


def _clean_response_object(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if hasattr(obj, "dict"):
        return obj.dict()

    if isinstance(obj, dict):
        return {
            key: _clean_response_object(value)
            for key, value in obj.items()
        }

    if hasattr(obj, "__dict__"):
        return {
            key: _clean_response_object(value)
            for key, value in vars(obj).items()
            if not key.startswith("_")
        }

    return obj


def analyze_with_jev(state: StockState) -> JEVResult:

    response = client.system_one(
        state=state.to_dict(),
        questions={

            "technical_trend": Choice(
                instructions=(
                    "Classify the current technical trend using ONLY "
                    "the supplied technical indicators and price/volume data. "
                    "Do not infer missing information."
                ),
                criteria={
                    "bullish": (
                        "The supplied technical evidence is predominantly "
                        "upward/positive."
                    ),
                    "neutral": (
                        "The supplied technical evidence is mixed or insufficient."
                    ),
                    "bearish": (
                        "The supplied technical evidence is predominantly "
                        "downward/negative."
                    ),
                },
            ),

            "technical_strength": Score(
                instructions=(
                    "Score the strength of the technical setup using ONLY "
                    "the supplied technical indicators. Do not treat missing "
                    "values as negative evidence."
                ),
                criteria=[
                    "Very weak",
                    "Weak",
                    "Neutral",
                    "Strong",
                    "Very strong",
                ],
            ),

            "bullish_setup": Noul(
                instructions=(
                    "Estimate the degree to which the supplied technical "
                    "evidence supports a bullish setup. This is a model "
                    "assessment of the supplied evidence, NOT a literal "
                    "probability of future returns."
                )
            ),

            "valuation": Choice(
                instructions=(
                    "Classify valuation using ONLY the supplied valuation "
                    "metrics. If the available valuation data is insufficient, "
                    "prefer reasonable rather than inventing missing evidence."
                ),
                criteria={
                    "attractive": (
                        "The supplied valuation metrics appear relatively attractive."
                    ),
                    "reasonable": (
                        "The supplied valuation metrics appear broadly neutral "
                        "or insufficient for a stronger classification."
                    ),
                    "expensive": (
                        "The supplied valuation metrics appear relatively expensive."
                    ),
                },
            ),

            "growth_profile": Choice(
                instructions=(
                    "Classify growth using ONLY the supplied revenue and EPS "
                    "growth metrics. Missing growth data must not be invented."
                ),
                criteria={
                    "strong": "The supplied growth metrics indicate strong growth.",
                    "moderate": (
                        "The supplied growth metrics indicate moderate growth "
                        "or mixed evidence."
                    ),
                    "weak": "The supplied growth metrics indicate weak growth.",
                },
            ),
        },
    )

    return JEVResult(
        symbol=state.symbol,
        choices=_clean_response_object(response.choices),
        scores=_clean_response_object(response.scores),
        nouls=_clean_response_object(response.nouls),
    )


def analyze_all_with_jev(states_list: list[StockState]) -> list[JEVResult]:

    results = []

    for state in states_list:

        try:
            result = analyze_with_jev(state)
            results.append(result)

            print(f"JEV finished: {state.symbol}")

        except Exception as e:

            print(f"JEV failed: {state.symbol} -> {e}")

    return results