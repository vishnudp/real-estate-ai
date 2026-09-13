from __future__ import annotations

from typing import Any, Dict


class InvestmentEngine:
    """
    Deterministic investment assessment layer.

    Combines:
    - infrastructure
    - comparable market evidence
    - valuation
    - growth
    - risk

    The engine does not invent missing property data.

    Important:
    - Target price/area are required for a definitive valuation decision.
    - Infrastructure score is normalized from the available infrastructure
      payload so the final investment metrics do not incorrectly return null.
    """

    def assess(
        self,
        property_data: Dict[str, Any],
        intelligence: Dict[str, Any],
        valuation: Dict[str, Any],
        comparables: Dict[str, Any],
    ) -> Dict[str, Any]:

        # ---------------------------------------------------------
        # Intelligence inputs
        # ---------------------------------------------------------

        infrastructure = intelligence.get(
            "infrastructure",
            {},
        ) or {}

        pricing = intelligence.get(
            "pricing",
            {},
        ) or {}

        growth = intelligence.get(
            "growth",
            {},
        ) or {}

        risk = intelligence.get(
            "risk",
            {},
        ) or {}

        # ---------------------------------------------------------
        # Infrastructure score
        #
        # Different layers may expose the same value using
        # different keys:
        #
        #   infrastructure.score
        #   infrastructure.infrastructure_score
        #   intelligence.infrastructure_score
        #
        # Normalize them here so metrics never become null when
        # the actual score is already available.
        # ---------------------------------------------------------

        infrastructure_score = self._get_infrastructure_score(
            intelligence=intelligence,
            infrastructure=infrastructure,
        )

        # ---------------------------------------------------------
        # Growth
        # ---------------------------------------------------------

        growth_score = growth.get(
            "score"
        )

        growth_assessment = growth.get(
            "assessment",
            "unknown",
        )

        growth_horizon = growth.get(
            "horizon"
        )

        growth_confidence = self._safe_float(
            growth.get(
                "confidence",
                0.0,
            )
        )

        # ---------------------------------------------------------
        # Risk
        # ---------------------------------------------------------

        risk_score = risk.get(
            "score"
        )

        risk_level = risk.get(
            "risk_level",
            "unknown",
        )

        risk_assessment = risk.get(
            "assessment"
        )

        risk_confidence = self._safe_float(
            risk.get(
                "confidence",
                0.0,
            )
        )

        # ---------------------------------------------------------
        # Overall intelligence assessment
        # ---------------------------------------------------------

        assessment = intelligence.get(
            "assessment",
            "unknown",
        )

        # ---------------------------------------------------------
        # Comparable metrics
        # ---------------------------------------------------------

        comparable_count = pricing.get(
            "priced_comparables"
        )

        if comparable_count is None:
            comparable_count = comparables.get(
                "count",
                comparables.get(
                    "comparable_count",
                    0,
                ),
            )

        comparable_count = self._safe_int(
            comparable_count
        )

        median_price = pricing.get(
            "median_price"
        )

        if median_price is None:
            median_price = (
                comparables
                .get("metrics", {})
                .get("median_price")
            )

        average_price = pricing.get(
            "average_price"
        )

        if average_price is None:
            average_price = (
                comparables
                .get("metrics", {})
                .get("average_price")
            )

        average_price_per_area = pricing.get(
            "average_price_per_area"
        )

        if average_price_per_area is None:
            average_price_per_area = (
                comparables
                .get("metrics", {})
                .get("average_price_per_area")
            )

        price_range = pricing.get(
            "price_range"
        )

        # ---------------------------------------------------------
        # Output buckets
        # ---------------------------------------------------------

        strengths: list[str] = []
        risks_list: list[str] = []
        considerations: list[str] = []

        # ---------------------------------------------------------
        # Infrastructure
        # ---------------------------------------------------------

        if infrastructure_score is not None:

            if infrastructure_score >= 80:

                strengths.append(
                    "Strong overall infrastructure profile"
                )

            elif infrastructure_score >= 60:

                strengths.append(
                    "Moderate overall infrastructure profile"
                )

            else:

                risks_list.append(
                    "Weak overall infrastructure profile"
                )

        for item in infrastructure.get(
            "strengths",
            [],
        ):

            if item not in strengths:
                strengths.append(item)

        for item in infrastructure.get(
            "weaknesses",
            [],
        ):

            if item not in risks_list:
                risks_list.append(item)

        # ---------------------------------------------------------
        # Comparable market evidence
        # ---------------------------------------------------------

        if comparable_count >= 2:

            message = (
                "Multiple priced comparable properties "
                "support the market view"
            )

            if message not in strengths:
                strengths.append(message)

        elif comparable_count == 1:

            considerations.append(
                "Only one priced comparable is available"
            )

        else:

            risks_list.append(
                "Insufficient priced comparable evidence"
            )

        if median_price is not None:

            strengths.append(
                "Comparable market pricing is available"
            )

        # ---------------------------------------------------------
        # Growth
        # ---------------------------------------------------------

        if growth_score is not None:

            if growth_score >= 75:

                strengths.append(
                    "Positive growth potential"
                )

            elif growth_score >= 55:

                considerations.append(
                    "Moderate growth potential"
                )

            else:

                risks_list.append(
                    "Weak growth potential"
                )

        if growth_assessment in {
            "positive",
            "strong",
            "high",
        }:

            if "Positive growth potential" not in strengths:

                strengths.append(
                    "Positive growth potential"
                )

        for item in growth.get(
            "signals",
            [],
        ):

            if item not in strengths:
                strengths.append(item)

        for item in growth.get(
            "risks",
            [],
        ):

            if item not in risks_list:
                risks_list.append(item)

        # ---------------------------------------------------------
        # Risk
        # ---------------------------------------------------------

        if risk_score is not None:

            if risk_score >= 70:

                risks_list.append(
                    "High investment risk based on available evidence"
                )

            elif risk_score >= 45:

                considerations.append(
                    "Moderate investment risk"
                )

            else:

                strengths.append(
                    "Relatively low investment risk"
                )

        if risk_level in {
            "high",
            "very_high",
        }:

            risk_message = (
                "Elevated investment risk"
            )

            if risk_message not in risks_list:

                risks_list.append(
                    risk_message
                )

        elif risk_level == "moderate":

            risk_message = (
                "Moderate investment risk"
            )

            if risk_message not in considerations:

                considerations.append(
                    risk_message
                )

        # ---------------------------------------------------------
        # Target property data
        # ---------------------------------------------------------

        target_price = property_data.get(
            "price"
        )

        target_area = property_data.get(
            "area"
        )

        target_bedrooms = property_data.get(
            "bedrooms"
        )

        if target_price is None:

            risks_list.append(
                "Target property asking price is unavailable"
            )

        if target_area is None:

            risks_list.append(
                "Target property area is unavailable"
            )

        if not target_bedrooms:

            risks_list.append(
                "Bedroom configuration is unavailable"
            )

        # ---------------------------------------------------------
        # Valuation
        # ---------------------------------------------------------

        valuation_available = bool(
            valuation.get(
                "available",
                False,
            )
        )

        upside = valuation.get(
            "upside_percent"
        )

        if valuation_available:

            if upside is not None:

                if upside >= 15:

                    strengths.append(
                        "Estimated valuation indicates meaningful potential upside"
                    )

                elif upside < 0:

                    risks_list.append(
                        "Estimated valuation indicates potential downside"
                    )

                else:

                    considerations.append(
                        "Estimated valuation indicates limited upside"
                    )

        else:

            considerations.append(
                "Purchase-price valuation cannot currently be completed reliably"
            )

        # ---------------------------------------------------------
        # Base recommendation
        # ---------------------------------------------------------

        if assessment in {
            "highly_attractive",
            "attractive",
        }:

            recommendation = "attractive"

        elif assessment == "moderately_attractive":

            recommendation = "moderately_attractive"

        elif assessment == "weak":

            recommendation = "weak"

        else:

            recommendation = "insufficient_data"

        # ---------------------------------------------------------
        # Risk adjustment
        # ---------------------------------------------------------

        if risk_level in {
            "high",
            "very_high",
        }:

            if recommendation == "attractive":

                recommendation = "moderately_attractive"

            elif recommendation == "moderately_attractive":

                recommendation = "weak"

        # ---------------------------------------------------------
        # Missing pricing protection
        #
        # Even if infrastructure/growth/risk look positive,
        # do not call the property a definitive investment while
        # the actual unit price or area is missing.
        # ---------------------------------------------------------

        missing_pricing_data = (
            target_price is None
            or target_area is None
        )

        if missing_pricing_data:

            decision = (
                "promising_but_requires_pricing_data"
            )

        else:

            decision = recommendation

        # ---------------------------------------------------------
        # Project name
        # ---------------------------------------------------------

        project_name = (
            property_data.get(
                "project_name"
            )
            or property_data.get(
                "title"
            )
            or "This property"
        )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        if decision == "promising_but_requires_pricing_data":

            summary = (
                f"{project_name} appears "
                f"{recommendation.replace('_', ' ')} "
                "based on its infrastructure, comparable-market, "
                "growth and risk evidence, but a definitive "
                "investment decision requires the actual unit "
                "price and property area."
            )

        elif decision == "attractive":

            summary = (
                f"{project_name} appears attractive based on "
                "the available infrastructure, comparable, "
                "valuation, growth and risk evidence."
            )

        elif decision == "moderately_attractive":

            summary = (
                f"{project_name} appears moderately attractive "
                "based on the available infrastructure, "
                "market, growth and risk evidence."
            )

        elif decision == "weak":

            summary = (
                f"{project_name} currently presents a relatively "
                "weak investment profile based on the available "
                "infrastructure, market, growth and risk evidence."
            )

        else:

            summary = (
                f"There is insufficient data to make a reliable "
                f"investment assessment for {project_name}."
            )

        # ---------------------------------------------------------
        # Deduplicate output
        # ---------------------------------------------------------

        strengths = list(
            dict.fromkeys(strengths)
        )

        risks_list = list(
            dict.fromkeys(risks_list)
        )

        considerations = list(
            dict.fromkeys(considerations)
        )

        # ---------------------------------------------------------
        # Confidence
        #
        # Keep the confidence calculation conservative.
        # Missing valuation data should reduce confidence rather
        # than being treated as full confidence.
        # ---------------------------------------------------------

        intelligence_confidence = self._safe_float(
            intelligence.get(
                "confidence",
                0.0,
            )
        )

        valuation_confidence = self._safe_float(
            valuation.get(
                "confidence",
                0.0,
            )
        )

        confidence_components = [
            intelligence_confidence,
            growth_confidence,
            risk_confidence,
            valuation_confidence,
        ]

        confidence_components = [
            value
            for value in confidence_components
            if value is not None
        ]

        if confidence_components:

            confidence = round(
                sum(confidence_components)
                / len(confidence_components),
                2,
            )

        else:

            confidence = 0.0

        # ---------------------------------------------------------
        # Final result
        # ---------------------------------------------------------
                # ---------------------------------------------------------
        # Investment score
        #
        # Deterministic score derived from the already calculated
        # investment dimensions.
        #
        # Higher is better.
        # Risk is inverted because RiskEngine uses:
        # higher score = higher risk.
        # ---------------------------------------------------------

        score_components = []

        if infrastructure_score is not None:
            score_components.append(
                (float(infrastructure_score), 0.20)
            )

        if growth_score is not None:
            score_components.append(
                (float(growth_score), 0.25)
            )

        if risk_score is not None:
            score_components.append(
                (100.0 - float(risk_score), 0.20)
            )

        if valuation.get("available", False):
            valuation_score = valuation.get(
                "valuation_score"
            )

            if valuation_score is not None:
                score_components.append(
                    (float(valuation_score), 0.25)
                )

        if comparable_count >= 5:
            comparable_score = 100.0

        elif comparable_count >= 3:
            comparable_score = 80.0

        elif comparable_count >= 1:
            comparable_score = 60.0

        else:
            comparable_score = 30.0

        score_components.append(
            (comparable_score, 0.10)
        )

        if score_components:

            total_weight = sum(
                weight
                for _, weight in score_components
            )

            investment_score = (
                sum(
                    value * weight
                    for value, weight in score_components
                )
                / total_weight
            )

            investment_score = round(
                max(
                    0.0,
                    min(100.0, investment_score),
                ),
                2,
            )

        else:

            investment_score = None

        return {
            "score": investment_score,

            "decision": decision,

            "recommendation": recommendation,

            "summary": summary,

            "strengths": strengths,

            "risks": risks_list,

            "considerations": considerations,

            "metrics": {
                "infrastructure_score": infrastructure_score,
                "growth_score": growth_score,
                "growth_assessment": growth_assessment,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "comparable_count": comparable_count,
                "median_comparable_price": median_price,
                "average_comparable_price": average_price,
                "average_price_per_area": average_price_per_area,
                "price_range": price_range,
            },

            "valuation": {
                "available": valuation_available,

                "estimated_value": valuation.get(
                    "estimated_value"
                ),

                "fair_value_low": valuation.get(
                    "fair_value_low"
                ),

                "fair_value_high": valuation.get(
                    "fair_value_high"
                ),

                "upside_percent": upside,

                "confidence": valuation.get(
                    "confidence"
                ),

                "reason": valuation.get(
                    "reason"
                ),
            },

            "growth": {
                "score": growth_score,

                "assessment": growth_assessment,

                "horizon": growth_horizon,

                "confidence": growth_confidence,
            },

            "risk": {
                "score": risk_score,

                "risk_level": risk_level,

                "assessment": risk_assessment,

                "confidence": risk_confidence,
            },

            "confidence": confidence,
        }

    # =============================================================
    # Helpers
    # =============================================================

    @staticmethod
    def _get_infrastructure_score(
        intelligence: Dict[str, Any],
        infrastructure: Dict[str, Any],
    ) -> float | None:
        """
        Resolve infrastructure score from all supported locations.

        Priority:

        1. intelligence.infrastructure.score
        2. intelligence.infrastructure.infrastructure_score
        3. intelligence.infrastructure_score

        This handles the current infrastructure engine output,
        which contains:

            {
                "infrastructure_score": 71.55,
                ...
            }

        while the investment engine previously only looked for:

            infrastructure["score"]

        That mismatch caused:

            "infrastructure_score": null
        """

        score = infrastructure.get(
            "score"
        )

        if score is None:

            score = infrastructure.get(
                "infrastructure_score"
            )

        if score is None:

            score = intelligence.get(
                "infrastructure_score"
            )

        return InvestmentEngine._safe_float(
            score
        )

    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float | None:
        """
        Safely convert a value to float.

        Returns None for:
        - None
        - empty strings
        - invalid values
        """

        if value is None:
            return None

        if isinstance(value, bool):
            return float(value)

        try:

            if isinstance(value, str):

                value = value.strip()

                if not value:
                    return None

            return float(value)

        except (
            TypeError,
            ValueError,
        ):

            return None

    @staticmethod
    def _safe_int(
        value: Any,
    ) -> int:
        """
        Safely convert a value to int.
        """

        if value is None:
            return 0

        try:
            return int(value)

        except (
            TypeError,
            ValueError,
        ):

            return 0
investment_engine = InvestmentEngine()
