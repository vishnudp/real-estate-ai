from __future__ import annotations

from statistics import median
from typing import Any


class ValuationEngine:
    """
    Simple deterministic valuation engine for the POC.

    Uses comparable properties to estimate fair value.
    The LLM is intentionally not used for calculations.
    """

    def __init__(self) -> None:
        pass

    def calculate_valuation(
        self,
        target: dict[str, Any],
        comparables: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not target:
            return self._unavailable(
                "Target property information is unavailable"
            )

        target_price = target.get("price")
        target_area = target.get("area")

        priced = [
            item
            for item in comparables
            if self._valid_number(item.get("price"))
        ]

        if not priced:
            return self._unavailable(
                "No priced comparable properties are available"
            )

        # ---------------------------------------------------------
        # CASE 1:
        # Target area is available
        # ---------------------------------------------------------
        if self._valid_number(target_area):

            price_per_area_values = []

            for item in priced:
                area = item.get("area")
                price = item.get("price")

                if (
                    self._valid_number(area)
                    and float(area) > 0
                    and self._valid_number(price)
                ):
                    price_per_area_values.append(
                        float(price) / float(area)
                    )

            if not price_per_area_values:
                return self._unavailable(
                    "Comparable properties do not contain usable area data"
                )

            median_price_per_area = median(
                price_per_area_values
            )

            estimated_value = (
                median_price_per_area * float(target_area)
            )

            fair_low = estimated_value * 0.90
            fair_high = estimated_value * 1.10

            upside = None

            if self._valid_number(target_price):
                upside = (
                    (estimated_value - float(target_price))
                    / float(target_price)
                ) * 100

            valuation_score = self._valuation_score(
                target_price=target_price,
                estimated_value=estimated_value,
            )

            confidence = self._confidence(
                comparable_count=len(priced),
                has_target_price=self._valid_number(target_price),
                has_target_area=True,
            )

            return {
                "available": True,
                "method": "median_comparable_price_per_area",
                "estimated_value": round(estimated_value, 2),
                "fair_value_low": round(fair_low, 2),
                "fair_value_high": round(fair_high, 2),
                "target_price": target_price,
                "target_area": target_area,
                "upside_percent": (
                    round(upside, 2)
                    if upside is not None
                    else None
                ),
                "valuation_score": valuation_score,
                "confidence": confidence,
                "comparable_count": len(priced),
                "limitations": [],
            }

        # ---------------------------------------------------------
        # CASE 2:
        # Target area unavailable
        #
        # We cannot calculate a defensible property-level
        # valuation because size is unknown.
        # ---------------------------------------------------------

        return self._unavailable(
            "Target property area is unavailable; "
            "fair value cannot be calculated reliably",
            confidence=self._confidence(
                comparable_count=len(priced),
                has_target_price=self._valid_number(target_price),
                has_target_area=False,
            ),
            comparable_count=len(priced),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _valid_number(value: Any) -> bool:
        if value is None:
            return False

        try:
            number = float(value)
            return number == number  # NaN check
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _valuation_score(
        target_price: Any,
        estimated_value: float,
    ) -> int | None:

        if not ValuationEngine._valid_number(target_price):
            return None

        target_price = float(target_price)

        if target_price <= 0:
            return None

        discount = (
            (estimated_value - target_price)
            / estimated_value
        ) * 100

        if discount >= 20:
            score = 95
        elif discount >= 15:
            score = 90
        elif discount >= 10:
            score = 85
        elif discount >= 5:
            score = 78
        elif discount >= 0:
            score = 70
        elif discount >= -5:
            score = 60
        elif discount >= -10:
            score = 50
        elif discount >= -15:
            score = 40
        else:
            score = 30

        return score

    @staticmethod
    def _confidence(
        comparable_count: int,
        has_target_price: bool,
        has_target_area: bool,
    ) -> float:

        confidence = 0.20

        if comparable_count >= 1:
            confidence += 0.15

        if comparable_count >= 3:
            confidence += 0.15

        if comparable_count >= 5:
            confidence += 0.10

        if has_target_area:
            confidence += 0.20

        if has_target_price:
            confidence += 0.20

        return round(min(confidence, 1.0), 2)

    @staticmethod
    def _unavailable(
        reason: str,
        confidence: float = 0.20,
        comparable_count: int = 0,
    ) -> dict[str, Any]:

        return {
            "available": False,
            "method": None,
            "estimated_value": None,
            "fair_value_low": None,
            "fair_value_high": None,
            "target_price": None,
            "target_area": None,
            "upside_percent": None,
            "valuation_score": None,
            "confidence": confidence,
            "comparable_count": comparable_count,
            "reason": reason,
            "limitations": [
                reason
            ],
        }


valuation_engine = ValuationEngine()