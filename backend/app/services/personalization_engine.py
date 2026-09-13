from __future__ import annotations

from typing import Any, Dict


class PersonalizationEngine:
    """
    Deterministic investor-personalization layer.

    This engine does NOT change the underlying property analysis.

    It evaluates:

    - investment recommendation
    - risk profile
    - growth potential
    - investment horizon
    - investor goal
    - investor risk tolerance
    - budget
    - target return
    - geographic preferences
    - property-type preferences
    - rental-income priority
    - capital-growth priority

    The result answers:

        "How suitable is this property for this investor?"

    rather than:

        "Is this property objectively attractive?"
    """

    # =============================================================
    # Public API
    # =============================================================

    def assess(
        self,
        property_data: Dict[str, Any],
        investment: Dict[str, Any],
        investor_profile: Dict[str, Any],
    ) -> Dict[str, Any]:

        investor_profile = investor_profile or {}
        investment = investment or {}
        property_data = property_data or {}

        # ---------------------------------------------------------
        # Investor preferences
        # ---------------------------------------------------------

        investment_goal = self._normalize(
            investor_profile.get(
                "investment_goal"
            )
        )

        risk_tolerance = self._normalize(
            investor_profile.get(
                "risk_tolerance"
            )
        )

        investment_horizon = self._normalize(
            investor_profile.get(
                "investment_horizon"
            )
        )

        budget = self._safe_float(
            investor_profile.get(
                "budget"
            )
        )

        target_return = self._safe_float(
            investor_profile.get(
                "target_return_percent"
            )
        )

        preferred_countries = self._normalize_list(
            investor_profile.get(
                "preferred_countries",
                [],
            )
        )

        preferred_cities = self._normalize_list(
            investor_profile.get(
                "preferred_cities",
                [],
            )
        )

        preferred_property_types = self._normalize_list(
            investor_profile.get(
                "preferred_property_types",
                [],
            )
        )

        preferred_bedrooms = investor_profile.get(
            "preferred_bedrooms"
        )

        yield_priority = self._safe_float(
            investor_profile.get(
                "yield_priority",
                0.5,
            )
        )

        growth_priority = self._safe_float(
            investor_profile.get(
                "growth_priority",
                0.5,
            )
        )

        # ---------------------------------------------------------
        # Property information
        # ---------------------------------------------------------

        property_country = self._normalize(
            property_data.get(
                "country"
            )
        )

        property_city = self._normalize(
            property_data.get(
                "city"
            )
        )

        property_type = self._normalize(
            property_data.get(
                "property_type"
            )
        )

        property_price = self._safe_float(
            property_data.get(
                "price"
            )
        )

        property_bedrooms = property_data.get(
            "bedrooms"
        )

        # ---------------------------------------------------------
        # Investment analysis
        # ---------------------------------------------------------

        recommendation = self._normalize(
            investment.get(
                "recommendation"
            )
        )

        decision = self._normalize(
            investment.get(
                "decision"
            )
        )

        metrics = investment.get(
            "metrics",
            {},
        ) or {}

        infrastructure_score = self._safe_float(
            metrics.get(
                "infrastructure_score"
            )
        )

        growth_score = self._safe_float(
            metrics.get(
                "growth_score"
            )
        )

        risk_score = self._safe_float(
            metrics.get(
                "risk_score"
            )
        )

        risk_level = self._normalize(
            metrics.get(
                "risk_level"
            )
        )

        valuation = investment.get(
            "valuation",
            {},
        ) or {}

        valuation_available = bool(
            valuation.get(
                "available",
                False,
            )
        )

        upside_percent = self._safe_float(
            valuation.get(
                "upside_percent"
            )
        )

        # ---------------------------------------------------------
        # Scoring
        # ---------------------------------------------------------

        score = 50.0

        strengths: list[str] = []
        concerns: list[str] = []
        reasons: list[str] = []

        # ---------------------------------------------------------
        # Base investment recommendation
        # ---------------------------------------------------------

        recommendation_scores = {
            "highly_attractive": 25,
            "attractive": 20,
            "moderately_attractive": 10,
            "weak": -20,
            "insufficient_data": -10,
        }

        score += recommendation_scores.get(
            recommendation,
            0,
        )

        # ---------------------------------------------------------
        # Risk tolerance matching
        # ---------------------------------------------------------

        risk_match = self._evaluate_risk_match(
            investor_risk_tolerance=risk_tolerance,
            property_risk_level=risk_level,
        )

        score += risk_match["score"]

        if risk_match["reason"]:

            if risk_match["matched"]:
                strengths.append(
                    risk_match["reason"]
                )
            else:
                concerns.append(
                    risk_match["reason"]
                )

        # ---------------------------------------------------------
        # Investment goal
        # ---------------------------------------------------------

        goal_result = self._evaluate_goal(
            investment_goal=investment_goal,
            growth_score=growth_score,
            upside_percent=upside_percent,
            valuation_available=valuation_available,
            yield_priority=yield_priority,
            growth_priority=growth_priority,
        )

        score += goal_result["score"]

        for item in goal_result["strengths"]:

            if item not in strengths:
                strengths.append(item)

        for item in goal_result["concerns"]:

            if item not in concerns:
                concerns.append(item)

        # ---------------------------------------------------------
        # Investment horizon
        # ---------------------------------------------------------

        horizon_result = self._evaluate_horizon(
            investor_horizon=investment_horizon,
            investment=investment,
            growth_score=growth_score,
        )

        score += horizon_result["score"]

        if horizon_result["reason"]:

            if horizon_result["matched"]:
                strengths.append(
                    horizon_result["reason"]
                )
            else:
                concerns.append(
                    horizon_result["reason"]
                )

        # ---------------------------------------------------------
        # Budget
        # ---------------------------------------------------------

        if budget is not None:

            if property_price is not None:

                if property_price <= budget:

                    score += 10

                    strengths.append(
                        "Property price fits within the investor's budget"
                    )

                else:

                    score -= 20

                    concerns.append(
                        "Property price exceeds the investor's budget"
                    )

            else:

                score -= 5

                concerns.append(
                    "Property price is unavailable, so budget fit cannot be confirmed"
                )

        # ---------------------------------------------------------
        # Country preference
        # ---------------------------------------------------------

        if preferred_countries:

            if property_country in preferred_countries:

                score += 8

                strengths.append(
                    "Property country matches the investor's geographic preference"
                )

            else:

                score -= 8

                concerns.append(
                    "Property country does not match the investor's preferred countries"
                )

        # ---------------------------------------------------------
        # City preference
        # ---------------------------------------------------------

        if preferred_cities:

            if property_city in preferred_cities:

                score += 5

                strengths.append(
                    "Property city matches the investor's geographic preference"
                )

            else:

                score -= 5

                concerns.append(
                    "Property city does not match the investor's preferred cities"
                )

        # ---------------------------------------------------------
        # Property type preference
        # ---------------------------------------------------------

        if preferred_property_types:

            if property_type in preferred_property_types:

                score += 8

                strengths.append(
                    "Property type matches the investor's preference"
                )

            else:

                score -= 8

                concerns.append(
                    "Property type does not match the investor's preferred property types"
                )

        # ---------------------------------------------------------
        # Bedroom preference
        # ---------------------------------------------------------

        if preferred_bedrooms is not None:

            if property_bedrooms is not None:

                if property_bedrooms == preferred_bedrooms:

                    score += 5

                    strengths.append(
                        "Bedroom configuration matches the investor's preference"
                    )

                else:

                    score -= 5

                    concerns.append(
                        "Bedroom configuration does not match the investor's preference"
                    )

            else:

                concerns.append(
                    "Bedroom configuration is unavailable, so bedroom preference cannot be confirmed"
                )

        # ---------------------------------------------------------
        # Target return
        # ---------------------------------------------------------

        if target_return is not None:

            if upside_percent is not None:

                if upside_percent >= target_return:

                    score += 10

                    strengths.append(
                        "Available valuation evidence meets the investor's target return"
                    )

                else:

                    score -= 10

                    concerns.append(
                        "Available valuation evidence does not meet the investor's target return"
                    )

            else:

                concerns.append(
                    "Target return cannot be validated because property valuation is unavailable"
                )

        # ---------------------------------------------------------
        # Infrastructure
        # ---------------------------------------------------------

        if infrastructure_score is not None:

            if infrastructure_score >= 75:

                score += 5

                strengths.append(
                    "Strong infrastructure supports the investor's property fit"
                )

            elif infrastructure_score < 50:

                score -= 5

                concerns.append(
                    "Infrastructure profile is relatively weak"
                )

        # ---------------------------------------------------------
        # Growth
        # ---------------------------------------------------------

        if growth_score is not None:

            if growth_score >= 75:

                if investment_goal in {
                    "capital_growth",
                    "capital_appreciation",
                    "balanced",
                }:

                    score += 7

                    strengths.append(
                        "Positive growth potential aligns with the investor's objectives"
                    )

        # ---------------------------------------------------------
        # Missing critical data
        # ---------------------------------------------------------

        if property_price is None:

            concerns.append(
                "Actual property price is unavailable"
            )

        if not valuation_available:

            concerns.append(
                "Property valuation is not currently available"
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
        # Fit classification
        # ---------------------------------------------------------

        if score >= 80:

            fit = "excellent_fit"

        elif score >= 65:

            fit = "good_fit"

        elif score >= 50:

            fit = "moderate_fit"

        elif score >= 35:

            fit = "weak_fit"

        else:

            fit = "poor_fit"

        # ---------------------------------------------------------
        # Data limitation
        #
        # Do not call a property an excellent fit if important
        # financial information is missing.
        # ---------------------------------------------------------

        if (
            property_price is None
            or not valuation_available
        ):

            if fit == "excellent_fit":
                fit = "good_fit"

        # ---------------------------------------------------------
        # Personalized recommendation
        # ---------------------------------------------------------

        personalized_recommendation = self._build_recommendation(
            fit=fit,
            decision=decision,
            investor_goal=investment_goal,
            risk_tolerance=risk_tolerance,
            property_name=(
                property_data.get(
                    "project_name"
                )
                or property_data.get(
                    "title"
                )
                or "This property"
            ),
        )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        property_name = (
            property_data.get(
                "project_name"
            )
            or property_data.get(
                "title"
            )
            or "This property"
        )

        summary = self._build_summary(
            property_name=property_name,
            fit=fit,
            investor_goal=investment_goal,
            risk_tolerance=risk_tolerance,
            concerns=concerns,
        )

        # ---------------------------------------------------------
        # Deduplicate
        # ---------------------------------------------------------

        strengths = list(
            dict.fromkeys(
                strengths
            )
        )

        concerns = list(
            dict.fromkeys(
                concerns
            )
        )

        reasons = list(
            dict.fromkeys(
                reasons
            )
        )

        # ---------------------------------------------------------
        # Confidence
        #
        # Personalization confidence depends on how much of the
        # investor profile is actually known.
        # ---------------------------------------------------------

        confidence = self._calculate_confidence(
            investor_profile=investor_profile,
            property_data=property_data,
            valuation=valuation,
            investment=investment,
        )

        # ---------------------------------------------------------
        # Final result
        # ---------------------------------------------------------

        return {
            "fit_score": score,

            "fit": fit,

            "recommendation": personalized_recommendation,

            "summary": summary,

            "strengths": strengths,

            "concerns": concerns,

            "investor_profile": {
                "investment_goal": investment_goal,
                "risk_tolerance": risk_tolerance,
                "investment_horizon": investment_horizon,
                "budget": budget,
                "target_return_percent": target_return,
                "preferred_countries": preferred_countries,
                "preferred_cities": preferred_cities,
                "preferred_property_types": preferred_property_types,
                "preferred_bedrooms": preferred_bedrooms,
                "yield_priority": yield_priority,
                "growth_priority": growth_priority,
            },

            "property_fit": {
                "country": property_data.get(
                    "country"
                ),
                "city": property_data.get(
                    "city"
                ),
                "property_type": property_data.get(
                    "property_type"
                ),
                "price": property_price,
                "bedrooms": property_bedrooms,
            },

            "metrics": {
                "infrastructure_score": infrastructure_score,
                "growth_score": growth_score,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "upside_percent": upside_percent,
                "valuation_available": valuation_available,
            },

            "confidence": confidence,
        }

    # =============================================================
    # Risk matching
    # =============================================================

    @staticmethod
    def _evaluate_risk_match(
        investor_risk_tolerance: str,
        property_risk_level: str,
    ) -> Dict[str, Any]:

        if not investor_risk_tolerance:

            return {
                "score": 0,
                "matched": False,
                "reason": "",
            }

        if not property_risk_level:

            return {
                "score": 0,
                "matched": False,
                "reason": "",
            }

        tolerance = investor_risk_tolerance
        risk = property_risk_level

        if tolerance == "conservative":

            if risk == "low":

                return {
                    "score": 10,
                    "matched": True,
                    "reason": (
                        "Property risk profile matches the investor's conservative risk tolerance"
                    ),
                }

            if risk == "moderate":

                return {
                    "score": -5,
                    "matched": False,
                    "reason": (
                        "Property carries more risk than the investor's conservative preference"
                    ),
                }

            return {
                "score": -15,
                "matched": False,
                "reason": (
                    "Property risk is high relative to the investor's conservative risk tolerance"
                ),
            }

        if tolerance == "moderate":

            if risk == "moderate":

                return {
                    "score": 10,
                    "matched": True,
                    "reason": (
                        "Property risk profile matches the investor's moderate risk tolerance"
                    ),
                }

            if risk == "low":

                return {
                    "score": 5,
                    "matched": True,
                    "reason": (
                        "Property risk profile is comfortably within the investor's moderate risk tolerance"
                    ),
                }

            return {
                "score": -10,
                "matched": False,
                "reason": (
                    "Property risk is higher than the investor's moderate risk tolerance"
                ),
            }

        if tolerance == "aggressive":

            if risk in {
                "high",
                "very_high",
            }:

                return {
                    "score": 8,
                    "matched": True,
                    "reason": (
                        "Property risk profile is compatible with the investor's aggressive risk tolerance"
                    ),
                }

            if risk == "moderate":

                return {
                    "score": 5,
                    "matched": True,
                    "reason": (
                        "Property's moderate risk profile is compatible with the investor's aggressive strategy"
                    ),
                }

            return {
                "score": 0,
                "matched": True,
                "reason": (
                    "Property risk is relatively low for the investor's aggressive strategy"
                ),
            }

        return {
            "score": 0,
            "matched": False,
            "reason": "",
        }

    # =============================================================
    # Goal evaluation
    # =============================================================

    @staticmethod
    def _evaluate_goal(
        investment_goal: str,
        growth_score: float | None,
        upside_percent: float | None,
        valuation_available: bool,
        yield_priority: float,
        growth_priority: float,
    ) -> Dict[str, Any]:

        result = {
            "score": 0,
            "strengths": [],
            "concerns": [],
        }

        if investment_goal in {
            "capital_growth",
            "capital_appreciation",
        }:

            if growth_score is not None:

                if growth_score >= 75:

                    result["score"] += 10

                    result["strengths"].append(
                        "Strong growth potential aligns with the investor's capital-growth objective"
                    )

                elif growth_score >= 55:

                    result["score"] += 4

                else:

                    result["score"] -= 8

                    result["concerns"].append(
                        "Growth potential is weaker than preferred for a capital-growth strategy"
                    )

            if growth_priority >= 0.7:

                result["strengths"].append(
                    "Investor places a high priority on capital growth"
                )

        elif investment_goal == "rental_income":

            if not valuation_available:

                result["concerns"].append(
                    "Rental-income suitability cannot be fully assessed without financial data"
                )

            if yield_priority >= 0.7:

                result["concerns"].append(
                    "Rental yield data should be provided before making an income-focused decision"
                )

        elif investment_goal == "balanced":

            if (
                growth_score is not None
                and growth_score >= 65
            ):

                result["score"] += 5

                result["strengths"].append(
                    "Growth profile is supportive of a balanced investment strategy"
                )

            if valuation_available:

                result["score"] += 5

        elif investment_goal == "lifestyle":

            result["score"] += 3

            result["strengths"].append(
                "Property can be evaluated partly on lifestyle and ownership preferences"
            )

        return result

    # =============================================================
    # Horizon evaluation
    # =============================================================

    @staticmethod
    def _evaluate_horizon(
        investor_horizon: str,
        investment: Dict[str, Any],
        growth_score: float | None,
    ) -> Dict[str, Any]:

        if not investor_horizon:

            return {
                "score": 0,
                "matched": False,
                "reason": "",
            }

        if investor_horizon in {
            "medium_term",
            "long_term",
        }:

            if growth_score is not None and growth_score >= 65:

                return {
                    "score": 7,
                    "matched": True,
                    "reason": (
                        "Positive growth profile is compatible with the investor's time horizon"
                    ),
                }

            return {
                "score": 0,
                "matched": False,
                "reason": (
                    "Available growth evidence does not strongly support the investor's time horizon"
                ),
            }

        if investor_horizon == "short_term":

            if investment.get(
                "valuation",
                {},
            ).get(
                "available",
                False,
            ):

                return {
                    "score": 5,
                    "matched": True,
                    "reason": (
                        "Available valuation data provides some support for the investor's shorter investment horizon"
                    ),
                }

            return {
                "score": -5,
                "matched": False,
                "reason": (
                    "Short-term investment suitability cannot be confirmed without valuation data"
                ),
            }

        return {
            "score": 0,
            "matched": False,
            "reason": "",
        }

    # =============================================================
    # Personalized recommendation
    # =============================================================

    @staticmethod
    def _build_recommendation(
        fit: str,
        decision: str,
        investor_goal: str,
        risk_tolerance: str,
        property_name: str,
    ) -> str:

        if fit == "excellent_fit":

            return (
                f"{property_name} is a strong match for this investor profile"
            )

        if fit == "good_fit":

            return (
                f"{property_name} is a good match for this investor profile"
            )

        if fit == "moderate_fit":

            return (
                f"{property_name} may be a reasonable match, subject to further financial validation"
            )

        if fit == "weak_fit":

            return (
                f"{property_name} has limited alignment with this investor profile"
            )

        return (
            f"{property_name} does not currently appear well aligned with this investor profile"
        )

    # =============================================================
    # Summary
    # =============================================================

    @staticmethod
    def _build_summary(
        property_name: str,
        fit: str,
        investor_goal: str,
        risk_tolerance: str,
        concerns: list[str],
    ) -> str:

        fit_text = fit.replace(
            "_",
            " ",
        )

        if investor_goal:

            goal_text = investor_goal.replace(
                "_",
                " ",
            )

            summary = (
                f"{property_name} is a {fit_text} for an investor "
                f"focused on {goal_text}"
            )

        else:

            summary = (
                f"{property_name} is a {fit_text} for the current investor profile"
            )

        if risk_tolerance:

            summary += (
                f" with {risk_tolerance} risk tolerance"
            )

        if concerns:

            summary += (
                ". However, some financial or preference data "
                "still needs to be validated."
            )

        else:

            summary += "."

        return summary

    # =============================================================
    # Confidence
    # =============================================================

    @staticmethod
    def _calculate_confidence(
        investor_profile: Dict[str, Any],
        property_data: Dict[str, Any],
        valuation: Dict[str, Any],
        investment: Dict[str, Any],
    ) -> float:

        fields = [
            "investment_goal",
            "risk_tolerance",
            "investment_horizon",
            "budget",
            "target_return_percent",
        ]

        supplied = 0

        for field in fields:

            value = investor_profile.get(
                field
            )

            if value is not None and value != "":

                supplied += 1

        profile_completeness = (
            supplied / len(fields)
        )

        investment_confidence = (
            PersonalizationEngine._safe_float(
                investment.get(
                    "confidence",
                    0.0,
                )
            )
            or 0.0
        )

        valuation_confidence = (
            PersonalizationEngine._safe_float(
                valuation.get(
                    "confidence",
                    0.0,
                )
            )
            or 0.0
        )

        confidence = (
            profile_completeness * 0.5
            + investment_confidence * 0.3
            + valuation_confidence * 0.2
        )

        return round(
            min(
                1.0,
                max(
                    0.0,
                    confidence,
                ),
            ),
            2,
        )

    # =============================================================
    # Helpers
    # =============================================================

    @staticmethod
    def _normalize(
        value: Any,
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        ).strip().lower()

    @staticmethod
    def _normalize_list(
        value: Any,
    ) -> list[str]:

        if not value:
            return []

        if isinstance(
            value,
            str,
        ):

            value = [
                value
            ]

        return [
            str(item)
            .strip()
            .lower()
            for item in value
            if item is not None
            and str(item).strip()
        ]

    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float | None:

        if value is None:
            return None

        try:

            if isinstance(
                value,
                str,
            ):

                value = value.strip()

                if not value:
                    return None

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return None
