from typing import Any

class DealEngine:
    """
    Deterministic deal-level decision engine.

    Combines the outputs of:
    - InvestmentEngine
    - ValuationEngine
    - GrowthEngine
    - RiskEngine
    - Infrastructure analysis
    - Comparable-market evidence

    This engine does not use an LLM and does not invent missing data.

    Important:
    - deal_score is an evidence-based score, not a guaranteed return.
    - decision describes the current attractiveness of the deal.
    - confidence describes confidence in the available evidence.
    """

    def assess(
        self,
        property_data: dict[str, Any],
        investment: dict[str, Any],
        valuation: dict[str, Any],
        growth: dict[str, Any],
        risk: dict[str, Any],
        intelligence: dict[str, Any],
        comparables: dict[str, Any],
    ) -> dict[str, Any]:

        investment_score = self._safe_float(
            investment.get("score")
        )

        valuation_score = self._safe_float(
            valuation.get("valuation_score")
        )

        growth_score = self._safe_float(
            growth.get("score")
        )

        risk_score = self._safe_float(
            risk.get("score")
        )

        infrastructure = intelligence.get(
            "infrastructure",
            {},
        ) or {}

        infrastructure_score = self._safe_float(
            infrastructure.get("score")
        )

        if infrastructure_score is None:
            infrastructure_score = self._safe_float(
                infrastructure.get(
                    "infrastructure_score"
                )
            )

        comparable_count = self._get_comparable_count(
            intelligence=intelligence,
            comparables=comparables,
        )

        valuation_confidence = self._safe_float(
            valuation.get("confidence")
        )

        growth_confidence = self._safe_float(
            growth.get("confidence")
        )

        risk_confidence = self._safe_float(
            risk.get("confidence")
        )

        # ---------------------------------------------------------
        # Deal score
        #
        # Investment score is the primary signal because it already
        # combines the major investment dimensions.
        #
        # The other signals provide deterministic reinforcement.
        # Missing signals are excluded and the score is normalized.
        # ---------------------------------------------------------

        weighted_scores: list[tuple[float, float]] = []

        if investment_score is not None:
            weighted_scores.append(
                (investment_score, 0.40)
            )

        if valuation_score is not None:
            weighted_scores.append(
                (valuation_score, 0.25)
            )

        if growth_score is not None:
            weighted_scores.append(
                (growth_score, 0.20)
            )

        if risk_score is not None:
            # Risk score is interpreted as:
            # higher = higher risk.
            risk_adjusted_score = 100.0 - risk_score

            weighted_scores.append(
                (risk_adjusted_score, 0.10)
            )

        if infrastructure_score is not None:
            weighted_scores.append(
                (infrastructure_score, 0.05)
            )

        deal_score = self._weighted_average(
            weighted_scores
        )

        # ---------------------------------------------------------
        # Evidence adjustments
        #
        # Do not manufacture confidence when evidence is missing.
        # ---------------------------------------------------------

        evidence_adjustment = 0.0

        if comparable_count == 0:
            evidence_adjustment -= 8

        elif comparable_count == 1:
            evidence_adjustment -= 4

        if not valuation.get(
            "available",
            False,
        ):
            evidence_adjustment -= 8

        if infrastructure_score is None:
            evidence_adjustment -= 4

        if deal_score is not None:
            deal_score += evidence_adjustment
            deal_score = max(
                0.0,
                min(100.0, deal_score),
            )

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------

        confidence_values = [
            value
            for value in [
                valuation_confidence,
                growth_confidence,
                risk_confidence,
            ]
            if value is not None
        ]

        if infrastructure_score is not None:
            confidence_values.append(
                1.0
            )

        if comparable_count >= 5:
            confidence_values.append(1.0)

        elif comparable_count >= 3:
            confidence_values.append(0.8)

        elif comparable_count >= 1:
            confidence_values.append(0.5)

        else:
            confidence_values.append(0.0)

        confidence = (
            sum(confidence_values)
            / len(confidence_values)
            if confidence_values
            else 0.0
        )

        confidence = round(
            max(0.0, min(1.0, confidence)),
            2,
        )

        # ---------------------------------------------------------
        # Decision
        # ---------------------------------------------------------

        decision = self._decision(
            deal_score=deal_score,
            confidence=confidence,
        )

        # ---------------------------------------------------------
        # Reasons
        # ---------------------------------------------------------

        strengths = []
        risks_list = []
        considerations = []

        if investment_score is not None:

            if investment_score >= 75:
                strengths.append(
                    "Investment analysis indicates strong attractiveness"
                )

            elif investment_score >= 60:
                strengths.append(
                    "Investment analysis indicates moderate attractiveness"
                )

            else:
                risks_list.append(
                    "Investment analysis indicates limited attractiveness"
                )

        if valuation.get("available"):

            upside = self._safe_float(
                valuation.get("upside_percent")
            )

            if upside is not None:

                if upside >= 15:
                    strengths.append(
                        "Property appears materially below estimated comparable value"
                    )

                elif upside >= 5:
                    strengths.append(
                        "Property shows positive valuation upside"
                    )

                elif upside < 0:
                    risks_list.append(
                        "Property is priced above estimated comparable value"
                    )

                else:
                    considerations.append(
                        "Valuation indicates limited upside"
                    )

        else:
            considerations.append(
                "Reliable property-level valuation is unavailable"
            )

        if growth_score is not None:

            if growth_score >= 75:
                strengths.append(
                    "Growth evidence is strong"
                )

            elif growth_score >= 55:
                considerations.append(
                    "Growth potential is moderate"
                )

            else:
                risks_list.append(
                    "Growth evidence is weak"
                )

        if risk_score is not None:

            if risk_score >= 70:

                risks_list.append(
                    "Overall investment risk is high"
                )

            elif risk_score >= 40:

                considerations.append(
                    "Investment risk is moderate"
                )

            else:

                strengths.append(
                    "Overall investment risk is relatively low"
                )

        if infrastructure_score is not None:

            if infrastructure_score >= 80:
                strengths.append(
                    "Infrastructure accessibility is strong"
                )

            elif infrastructure_score < 50:
                risks_list.append(
                    "Infrastructure accessibility is weak"
                )

        if comparable_count >= 5:
            strengths.append(
                "Strong comparable-market evidence is available"
            )

        elif comparable_count >= 3:
            strengths.append(
                "Multiple comparable properties support the market view"
            )

        elif comparable_count >= 2:
            considerations.append(
                "Two priced comparable properties are available"
            )

        elif comparable_count == 1:
            considerations.append(
                "Only one priced comparable is available"
            )

        else:
            risks_list.append(
                "No priced comparable evidence is available"
            )


        # ---------------------------------------------------------
        # Remove duplicate messages while preserving order.
        # ---------------------------------------------------------

        strengths = self._unique(strengths)
        risks_list = self._unique(risks_list)
        considerations = self._unique(
            considerations
        )

        reasons = (
            strengths[:3]
            + considerations[:2]
        )

        # If there are no positive reasons, expose the risks instead.
        if not reasons:
            reasons = risks_list[:3]

        return {
            "available": deal_score is not None,
            "deal_score": (
                round(deal_score, 2)
                if deal_score is not None
                else None
            ),
            "decision": decision,
            "confidence": confidence,
            "reasons": reasons,
            "strengths": strengths,
            "risks": risks_list,
            "considerations": considerations,
            "inputs": {
                "investment_score": investment_score,
                "valuation_score": valuation_score,
                "growth_score": growth_score,
                "risk_score": risk_score,
                "infrastructure_score": infrastructure_score,
                "comparable_count": comparable_count,
            },
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float | None:

        if value is None:
            return None

        try:
            number = float(value)

            if number != number:
                return None

            return number

        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _weighted_average(
        values: list[tuple[float, float]],
    ) -> float | None:

        if not values:
            return None

        total_weight = sum(
            weight
            for _, weight in values
        )

        if total_weight <= 0:
            return None

        weighted_total = sum(
            score * weight
            for score, weight in values
        )

        return (
            weighted_total
            / total_weight
        )

    @staticmethod
    def _get_comparable_count(
        intelligence: dict[str, Any],
        comparables: dict[str, Any],
    ) -> int:

        pricing = intelligence.get(
            "pricing",
            {},
        ) or {}

        value = pricing.get(
            "priced_comparables"
        )

        if value is None:
            value = comparables.get(
                "count"
            )

        if value is None:
            value = comparables.get(
                "comparable_count",
                0,
            )

        try:
            return max(
                0,
                int(value),
            )

        except (
            TypeError,
            ValueError,
        ):
            return 0

    @staticmethod
    def _decision(
        deal_score: float | None,
        confidence: float,
    ) -> str:

        if deal_score is None:
            return "insufficient_evidence"

        if confidence < 0.40:
            return "insufficient_evidence"

        if deal_score >= 80:
            return "strong"

        if deal_score >= 70:
            return "promising"

        if deal_score >= 55:
            return "moderate"

        if deal_score >= 40:
            return "weak"

        return "unattractive"

    @staticmethod
    def _unique(
        items: list[str],
    ) -> list[str]:

        result = []

        for item in items:
            if item not in result:
                result.append(item)

        return result

deal_engine = DealEngine()
