from typing import Any, Dict

class RiskEngine:
    """
    Deterministic property investment risk assessment.

    This engine evaluates risk using only available evidence from:
    - property data
    - infrastructure
    - comparables
    - valuation
    - growth

    It does not invent missing financial data and does not make
    a buy/sell recommendation.
    """

    def assess(
        self,
        property_data: Dict[str, Any],
        intelligence: Dict[str, Any],
        valuation: Dict[str, Any],
        comparables: Dict[str, Any],
        growth: Dict[str, Any],
    ) -> Dict[str, Any]:

        infrastructure = intelligence.get(
            "infrastructure",
            {},
        )

        pricing = intelligence.get(
            "pricing",
            {},
        )

        risks = []
        strengths = []

        # ---------------------------------------------------------
        # Risk category scores
        #
        # Higher score = higher risk.
        # ---------------------------------------------------------

        pricing_risk = 0.0
        valuation_risk = 0.0
        location_risk = 0.0
        market_risk = 0.0
        data_quality_risk = 0.0

        # ---------------------------------------------------------
        # Pricing risk
        # ---------------------------------------------------------

        target_price = property_data.get("price")

        if target_price is None:
            pricing_risk = 80.0

            risks.append(
                "Target property asking price is unavailable"
            )
        else:
            pricing_risk = 20.0

            strengths.append(
                "Target property asking price is available"
            )

        # ---------------------------------------------------------
        # Property area
        # ---------------------------------------------------------

        target_area = property_data.get("area")

        if target_area is None:
            pricing_risk = max(
                pricing_risk,
                70.0,
            )

            risks.append(
                "Target property area is unavailable"
            )

        # ---------------------------------------------------------
        # Valuation risk
        # ---------------------------------------------------------

        valuation_available = valuation.get(
            "available",
            False,
        )

        if not valuation_available:

            valuation_risk = 75.0

            reason = valuation.get(
                "reason"
            )

            if reason:
                risks.append(
                    f"Valuation unavailable: {reason}"
                )
            else:
                risks.append(
                    "Reliable property valuation is unavailable"
                )

        else:

            valuation_risk = 20.0

            strengths.append(
                "Property valuation is available"
            )

            upside = valuation.get(
                "upside_percent"
            )

            if upside is not None:

                if upside < 0:

                    valuation_risk = max(
                        valuation_risk,
                        80.0,
                    )

                    risks.append(
                        "Estimated valuation indicates potential downside"
                    )

                elif upside < 10:

                    valuation_risk = max(
                        valuation_risk,
                        50.0,
                    )

                    risks.append(
                        "Estimated valuation indicates limited upside"
                    )

                elif upside >= 15:

                    strengths.append(
                        "Estimated valuation indicates meaningful upside"
                    )

        # ---------------------------------------------------------
        # Infrastructure / location risk
        # ---------------------------------------------------------

        infrastructure_score = infrastructure.get(
            "score"
        )

        if infrastructure_score is None:
            infrastructure_score = infrastructure.get(
                "infrastructure_score"
            )

        if infrastructure_score is None:

            location_risk = 60.0

            risks.append(
                "Infrastructure evidence is unavailable"
            )

        elif infrastructure_score < 40:

            location_risk = 80.0

            risks.append(
                "Weak overall infrastructure accessibility"
            )

        elif infrastructure_score < 60:

            location_risk = 55.0

            risks.append(
                "Moderate infrastructure accessibility"
            )

        elif infrastructure_score < 80:

            location_risk = 30.0

            strengths.append(
                "Moderate-to-strong infrastructure accessibility"
            )

        else:

            location_risk = 10.0

            strengths.append(
                "Strong infrastructure accessibility"
            )

        # ---------------------------------------------------------
        # Infrastructure weaknesses
        # ---------------------------------------------------------

        weaknesses = infrastructure.get(
            "weaknesses",
            [],
        )

        for weakness in weaknesses:

            if weakness not in risks:
                risks.append(
                    weakness
                )

        # ---------------------------------------------------------
        # Comparable / market risk
        # ---------------------------------------------------------

        comparable_count = pricing.get(
            "priced_comparables",
            comparables.get(
                "count",
                0,
            ),
        )

        if comparable_count <= 0:

            market_risk = 80.0

            risks.append(
                "No priced comparable properties are available"
            )

        elif comparable_count == 1:

            market_risk = 60.0

            risks.append(
                "Only one priced comparable property is available"
            )

        elif comparable_count < 3:

            market_risk = 45.0

            risks.append(
                "Limited comparable-market evidence is available"
            )

        elif comparable_count < 5:

            market_risk = 30.0

            strengths.append(
                "Multiple priced comparable properties are available"
            )

        else:

            market_risk = 15.0

            strengths.append(
                "Strong comparable-market evidence is available"
            )

        # ---------------------------------------------------------
        # Comparable price dispersion
        # ---------------------------------------------------------

        price_range = pricing.get(
            "price_range"
        )

        average_price = pricing.get(
            "average_price"
        )

        if (
            price_range
            and average_price
            and average_price > 0
        ):

            minimum_price = price_range.get(
                "min"
            )

            maximum_price = price_range.get(
                "max"
            )

            if (
                minimum_price is not None
                and maximum_price is not None
            ):

                dispersion = (
                    maximum_price - minimum_price
                ) / average_price

                if dispersion > 0.50:

                    market_risk = max(
                        market_risk,
                        55.0,
                    )

                    risks.append(
                        "Comparable property prices show relatively high dispersion"
                    )

                elif dispersion < 0.30:

                    strengths.append(
                        "Comparable property pricing is relatively consistent"
                    )

        # ---------------------------------------------------------
        # Growth risk
        # ---------------------------------------------------------

        growth_score = growth.get(
            "score"
        )

        if growth_score is None:

            growth_risk = 50.0

            risks.append(
                "Growth evidence is unavailable"
            )

        elif growth_score < 40:

            growth_risk = 75.0

            risks.append(
                "Growth outlook is weak"
            )

        elif growth_score < 60:

            growth_risk = 50.0

            risks.append(
                "Growth outlook is moderate"
            )

        elif growth_score < 80:

            growth_risk = 30.0

            strengths.append(
                "Positive growth potential"
            )

        else:

            growth_risk = 15.0

            strengths.append(
                "Strong growth potential"
            )

        # ---------------------------------------------------------
        # Growth risks
        # ---------------------------------------------------------

        for item in growth.get(
            "risks",
            [],
        ):

            if item not in risks:
                risks.append(
                    item
                )

        # ---------------------------------------------------------
        # Data quality risk
        # ---------------------------------------------------------

        data_completeness = intelligence.get(
            "data_completeness"
        )

        if data_completeness is None:

            intelligence_confidence = intelligence.get(
                "confidence",
                0.0,
            )

            if intelligence_confidence >= 0.8:
                data_quality_risk = 20.0
            elif intelligence_confidence >= 0.6:
                data_quality_risk = 40.0
            else:
                data_quality_risk = 70.0

        else:

            if data_completeness >= 0.90:
                data_quality_risk = 10.0
            elif data_completeness >= 0.75:
                data_quality_risk = 25.0
            elif data_completeness >= 0.50:
                data_quality_risk = 50.0
            else:
                data_quality_risk = 75.0

        if data_quality_risk >= 50:

            risks.append(
                "Important property data is incomplete"
            )

        else:

            strengths.append(
                "Core property intelligence data is reasonably complete"
            )

        # ---------------------------------------------------------
        # Overall risk score
        #
        # Weighted average:
        #
        # Pricing       25%
        # Valuation     20%
        # Location      20%
        # Market        15%
        # Growth        10%
        # Data quality  10%
        # ---------------------------------------------------------

        risk_score = (
            pricing_risk * 0.25
            + valuation_risk * 0.20
            + location_risk * 0.20
            + market_risk * 0.15
            + growth_risk * 0.10
            + data_quality_risk * 0.10
        )

        risk_score = round(
            risk_score,
            2,
        )

        # ---------------------------------------------------------
        # Risk assessment
        # ---------------------------------------------------------

        if risk_score >= 70:

            risk_level = "high"
            assessment = "high_risk"

        elif risk_score >= 50:

            risk_level = "moderate"
            assessment = "moderate_risk"

        elif risk_score >= 30:

            risk_level = "low_moderate"
            assessment = "low_to_moderate_risk"

        else:

            risk_level = "low"
            assessment = "low_risk"

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------

        confidence_inputs = []

        if infrastructure_score is not None:
            confidence_inputs.append(1.0)

        if comparable_count:
            confidence_inputs.append(
                min(
                    comparable_count / 5,
                    1.0,
                )
            )

        if valuation_available:
            confidence_inputs.append(1.0)

        if growth_score is not None:
            confidence_inputs.append(
                growth.get(
                    "confidence",
                    0.5,
                )
            )

        if not confidence_inputs:

            confidence = 0.0

        else:

            confidence = sum(
                confidence_inputs
            ) / len(
                confidence_inputs
            )

        confidence = round(
            confidence,
            2,
        )

        # ---------------------------------------------------------
        # Deduplicate evidence
        # ---------------------------------------------------------

        risks = list(
            dict.fromkeys(
                risks
            )
        )

        strengths = list(
            dict.fromkeys(
                strengths
            )
        )

        # ---------------------------------------------------------
        # Summary
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

        summary = (
            f"{project_name} has a {risk_level} investment "
            f"risk profile with a risk score of "
            f"{risk_score}/100 based on the available "
            "pricing, valuation, location, market, growth "
            "and data-quality evidence."
        )

        return {
            "score": risk_score,
            "risk_level": risk_level,
            "assessment": assessment,
            "summary": summary,
            "strengths": strengths,
            "risks": risks,
            "risk_categories": {
                "pricing": round(
                    pricing_risk,
                    2,
                ),
                "valuation": round(
                    valuation_risk,
                    2,
                ),
                "location": round(
                    location_risk,
                    2,
                ),
                "market": round(
                    market_risk,
                    2,
                ),
                "growth": round(
                    growth_risk,
                    2,
                ),
                "data_quality": round(
                    data_quality_risk,
                    2,
                ),
            },
            "confidence": confidence,
        }

risk_engine = RiskEngine()
