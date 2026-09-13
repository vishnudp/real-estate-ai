from __future__ import annotations

from typing import Any


class GrowthEngine:
    """
    Deterministic growth-potential assessment layer.

    This engine does NOT predict future property prices or invent
    appreciation percentages.

    It evaluates available evidence that may support future growth,
    including:

    - infrastructure
    - comparable-market evidence
    - valuation
    - development/completion status
    - tourism accessibility
    - property positioning
    - data completeness

    The output is a growth-potential assessment, not a guaranteed
    investment return forecast.
    """

    def calculate_growth(
        self,
        property_data: dict[str, Any],
        infrastructure: dict[str, Any],
        comparables: dict[str, Any],
        valuation: dict[str, Any],
        intelligence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        intelligence = intelligence or {}

        signals: list[str] = []
        risks: list[str] = []

        score = 50.0

        # ---------------------------------------------------------
        # Infrastructure
        # ---------------------------------------------------------

        infrastructure_score = infrastructure.get(
            "infrastructure_score"
        )

        if infrastructure_score is None:
            infrastructure_score = infrastructure.get(
                "score"
            )

        if infrastructure_score is not None:

            if infrastructure_score >= 80:
                score += 15
                signals.append(
                    "Strong infrastructure accessibility supports growth potential"
                )

            elif infrastructure_score >= 60:
                score += 8
                signals.append(
                    "Moderate infrastructure accessibility supports growth potential"
                )

            elif infrastructure_score < 40:
                score -= 10
                risks.append(
                    "Weak infrastructure accessibility may limit growth potential"
                )

            else:
                score -= 3
                risks.append(
                    "Infrastructure profile is below a strong-growth threshold"
                )

        else:
            risks.append(
                "Infrastructure evidence is unavailable"
            )

        # ---------------------------------------------------------
        # Infrastructure categories
        # ---------------------------------------------------------

        categories = infrastructure.get(
            "categories",
            {}
        )

        strong_categories = 0
        weak_categories = 0

        for category, data in categories.items():

            if not isinstance(data, dict):
                continue

            category_score = data.get(
                "score"
            )

            if category_score is None:
                continue

            if category_score >= 80:
                strong_categories += 1

            elif category_score < 40:
                weak_categories += 1

        if strong_categories >= 3:
            score += 5
            signals.append(
                "Multiple infrastructure categories show strong accessibility"
            )

        if weak_categories >= 3:
            score -= 5
            risks.append(
                "Several infrastructure categories show weak accessibility"
            )

        # ---------------------------------------------------------
        # Comparable market evidence
        # ---------------------------------------------------------

        comparable_metrics = comparables.get(
            "metrics",
            {}
        )

        comparable_count = comparable_metrics.get(
            "priced_comparables"
        )

        if comparable_count is None:
            comparable_count = comparables.get(
                "comparable_count",
                comparables.get("count", 0),
            )

        average_price = comparable_metrics.get(
            "average_price"
        )

        median_price = comparable_metrics.get(
            "median_price"
        )

        average_price_per_area = comparable_metrics.get(
            "average_price_per_area"
        )

        if comparable_count >= 5:

            score += 10
            signals.append(
                "Strong comparable-market evidence is available"
            )

        elif comparable_count >= 3:

            score += 6
            signals.append(
                "Multiple comparable properties provide market evidence"
            )

        elif comparable_count == 1:

            score += 1
            risks.append(
                "Only one priced comparable is available"
            )

        else:

            score -= 8
            risks.append(
                "Insufficient comparable-market evidence"
            )

        if (
            average_price_per_area is not None
            and average_price_per_area > 0
        ):
            signals.append(
                "Comparable price-per-area data is available"
            )

        # ---------------------------------------------------------
        # Valuation
        # ---------------------------------------------------------

        valuation_available = valuation.get(
            "available",
            False,
        )

        upside = valuation.get(
            "upside_percent"
        )

        if valuation_available:

            if upside is not None:

                if upside >= 15:

                    score += 15
                    signals.append(
                        "Current valuation indicates meaningful potential upside"
                    )

                elif upside >= 5:

                    score += 8
                    signals.append(
                        "Current valuation indicates positive potential upside"
                    )

                elif upside >= 0:

                    score += 2
                    signals.append(
                        "Current valuation indicates limited positive upside"
                    )

                else:

                    score -= 10
                    risks.append(
                        "Current valuation indicates potential downside"
                    )

            else:

                score += 3
                signals.append(
                    "A valuation assessment is available"
                )

        else:

            risks.append(
                "Target property valuation is unavailable"
            )

        # ---------------------------------------------------------
        # Development / completion status
        # ---------------------------------------------------------

        status = (
            property_data.get("status")
            or ""
        )

        completion_date = property_data.get(
            "completion_date"
        )

        status_text = str(
            status
        ).lower()

        if any(
            keyword in status_text
            for keyword in [
                "off-plan",
                "under construction",
                "construction",
                "planned",
                "pre-launch",
                "launch",
            ]
        ):

            score += 5
            signals.append(
                "Development-stage positioning may provide growth potential"
            )

        elif any(
            keyword in status_text
            for keyword in [
                "completed",
                "ready",
                "ready to move",
            ]
        ):

            signals.append(
                "Completed property provides more mature market evidence"
            )

        if completion_date:

            signals.append(
                "A project completion date is available"
            )

        elif any(
            keyword in status_text
            for keyword in [
                "off-plan",
                "under construction",
                "construction",
                "planned",
            ]
        ):

            risks.append(
                "Development timing information is incomplete"
            )

        # ---------------------------------------------------------
        # Tourism
        # ---------------------------------------------------------

        tourism = categories.get(
            "tourism",
            {}
        )

        tourism_score = tourism.get(
            "score"
        ) if isinstance(tourism, dict) else None

        if tourism_score is not None:

            if tourism_score >= 80:

                score += 5
                signals.append(
                    "Strong tourism accessibility supports potential demand growth"
                )

            elif tourism_score < 40:

                score -= 3
                risks.append(
                    "Weak tourism accessibility may limit demand growth"
                )

        # ---------------------------------------------------------
        # Branded property positioning
        # ---------------------------------------------------------

        brands = property_data.get(
            "brands"
        )

        property_type = str(
            property_data.get(
                "property_type"
            )
            or ""
        ).lower()

        if brands:

            score += 3
            signals.append(
                "Branded property positioning may support future demand"
            )

        elif "branded" in property_type:

            score += 2
            signals.append(
                "Branded-residence positioning may support future demand"
            )

        # ---------------------------------------------------------
        # Data completeness
        # ---------------------------------------------------------

        data_completeness = intelligence.get(
            "data_completeness"
        )

        if data_completeness is not None:

            if data_completeness >= 0.8:

                score += 3

            elif data_completeness < 0.5:

                score -= 5
                risks.append(
                    "Limited property data reduces growth-assessment confidence"
                )

        # ---------------------------------------------------------
        # Clamp score
        # ---------------------------------------------------------

        score = max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

        score = round(
            score,
            2,
        )

        # ---------------------------------------------------------
        # Assessment
        # ---------------------------------------------------------

        if score >= 80:

            assessment = "strong_positive"

        elif score >= 65:

            assessment = "positive"

        elif score >= 50:

            assessment = "moderate"

        elif score >= 35:

            assessment = "weak"

        else:

            assessment = "negative"

        # ---------------------------------------------------------
        # Horizon
        # ---------------------------------------------------------

        if assessment in {
            "strong_positive",
            "positive",
        }:

            horizon = "medium_term"

        elif assessment == "moderate":

            horizon = "medium_to_long_term"

        else:

            horizon = "uncertain"

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------

        confidence_components = []

        if infrastructure_score is not None:
            confidence_components.append(1.0)

        if comparable_count and comparable_count >= 1:
            confidence_components.append(
                min(
                    comparable_count / 5,
                    1.0,
                )
            )

        if valuation_available:
            confidence_components.append(1.0)

        if data_completeness is not None:
            confidence_components.append(
                max(
                    0.0,
                    min(
                        float(data_completeness),
                        1.0,
                    ),
                )
            )

        if confidence_components:

            confidence = sum(
                confidence_components
            ) / len(
                confidence_components
            )

        else:

            confidence = 0.0

        confidence = round(
            confidence,
            2,
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

        if assessment == "strong_positive":

            summary = (
                f"{project_name} shows strong growth potential "
                "based on the available infrastructure, market "
                "and property evidence."
            )

        elif assessment == "positive":

            summary = (
                f"{project_name} shows positive growth potential "
                "based on the available market and location signals."
            )

        elif assessment == "moderate":

            summary = (
                f"{project_name} shows moderate growth potential, "
                "but additional market evidence is needed for a "
                "stronger growth outlook."
            )

        elif assessment == "weak":

            summary = (
                f"{project_name} currently shows limited growth "
                "potential based on the available evidence."
            )

        else:

            summary = (
                f"{project_name} currently shows negative or "
                "insufficient growth signals based on the available evidence."
            )

        return {
            "score": score,
            "assessment": assessment,
            "horizon": horizon,
            "summary": summary,
            "signals": signals,
            "risks": risks,
            "confidence": confidence,
            "metrics": {
                "infrastructure_score": infrastructure_score,
                "comparable_count": comparable_count,
                "average_comparable_price": average_price,
                "median_comparable_price": median_price,
                "average_price_per_area": average_price_per_area,
                "valuation_available": valuation_available,
                "valuation_upside_percent": upside,
            },
        }


growth_engine = GrowthEngine()
