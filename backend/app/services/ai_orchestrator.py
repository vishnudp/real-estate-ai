from __future__ import annotations

import json
import re
from typing import Any

from app.ai.llm_client import LLMClient

from app.services.ai_guardrails import AIGuardrails


class AIOrchestrator:
    """
    AI orchestration layer for the real-estate intelligence POC.

    Deterministic property facts and scores remain authoritative.

    Simple factual questions are answered deterministically.

    Analytical questions can use Ollama, but only with verified
    property intelligence supplied to the model.
    """

    SYSTEM_PROMPT = """
You are a real-estate property intelligence assistant.

Answer the user's question using ONLY the supplied verified
property intelligence.

Rules:

- Never invent facts.
- Never invent prices.
- Never invent areas.
- Never invent developers.
- Never invent locations.
- Never invent rental yields or returns.
- Never invent comparable properties.
- Never invent infrastructure information.
- Never change supplied scores.
- Never recalculate scores.
- Never recalculate valuation.
- Never guarantee investment returns.
- Never tell the user to definitely buy or sell.
- Never provide financial advice.
- If information is unavailable, say so clearly.

MOST IMPORTANT:

Return ONLY the answer that should be shown to the user.

DO NOT:

- explain your reasoning
- describe your analysis steps
- mention instructions
- mention JSON
- say "we are given"
- say "the user asks"
- say "let's analyze"
- say "the instructions say"
- expose internal reasoning
- repeat the user's question
- provide hidden chain-of-thought

Keep the answer natural and concise.

For simple questions, answer directly.

For investment questions, give a concise assessment based only on
the supplied investment, deal, growth and risk intelligence.

For risk questions, explain the actual supplied risks.

Do not provide unrelated property information.
""".strip()

    def __init__(
        self,
        llm_client: LLMClient | None = None,
    ) -> None:

        self.llm = (
            llm_client
            or LLMClient()
        )

        self.guardrails = AIGuardrails()

    # =========================================================
    # INTENT CLASSIFICATION
    # =========================================================

    def classify_intent(
        self,
        query: str,
    ) -> str:

        q = query.lower().strip()

        # -----------------------------------------------------
        # Combined purchase + risk question
        #
        # These should be treated as investment questions because
        # the user is asking whether they should purchase and also
        # wants to know the risks.
        # -----------------------------------------------------

        purchase_patterns = [
            "should i buy",
            "should we buy",
            "should i purchase",
            "should we purchase",
            "we need to purchase",
            "need to purchase",
            "good to buy",
            "good buy",
            "buy this property",
            "purchase this property",
            "worth buying",
            "worth purchasing",
        ]

        risk_patterns = [
            "risk",
            "risks",
            "risky",
            "any risk",
            "any risks",
            "what are the risks",
            "what risks",
            "risk with this property",
            "risks with this property",
            "risk associated",
            "risk involved",
            "risk included",
        ]

        has_purchase = any(
            pattern in q
            for pattern in purchase_patterns
        )

        has_risk = any(
            pattern in q
            for pattern in risk_patterns
        )

        if has_purchase and has_risk:
            return "property_investment_analysis"

        # -----------------------------------------------------
        # Developer
        # -----------------------------------------------------

        developer_patterns = [
            "who is the developer",
            "who developed",
            "who developed this",
            "developer of this property",
            "property developer",
        ]

        if any(
            pattern in q
            for pattern in developer_patterns
        ):
            return "property_developer"

        # -----------------------------------------------------
        # Price
        # -----------------------------------------------------

        price_patterns = [
            "what is the price",
            "what's the price",
            "how much is this property",
            "how much does this property cost",
            "asking price",
            "property price",
            "price of this property",
            "cost of this property",
            "how much is the property",
        ]

        if any(
            pattern in q
            for pattern in price_patterns
        ):
            return "property_price"

        # -----------------------------------------------------
        # Area
        # -----------------------------------------------------

        area_patterns = [
            "what is the area",
            "what's the area",
            "how big is this property",
            "property size",
            "how large is this property",
            "square feet",
            "sq ft",
            "area of this property",
        ]

        if any(
            pattern in q
            for pattern in area_patterns
        ):
            return "property_area"

        # -----------------------------------------------------
        # Location
        # -----------------------------------------------------

        location_patterns = [
            "where is this property",
            "where is the property",
            "property location",
            "where is it located",
            "which city is this property",
            "which country is this property",
            "location of this property",
        ]

        if any(
            pattern in q
            for pattern in location_patterns
        ):
            return "property_location"

        # -----------------------------------------------------
        # Risk
        # -----------------------------------------------------

        if has_risk:
            return "property_risk_analysis"

        # -----------------------------------------------------
        # Investment
        # -----------------------------------------------------

        investment_patterns = [
            "good investment",
            "good deal",
            "worth it",
            "investment potential",
            "investment opportunity",
            "why should i consider",
            "is this property good",
            "investment",
            "deal score",
            "should i invest",
            "should we invest",
        ]

        if any(
            pattern in q
            for pattern in investment_patterns
        ):
            return "property_investment_analysis"

        # -----------------------------------------------------
        # Comparison
        # -----------------------------------------------------

        comparison_patterns = [
            "compare",
            "comparison",
            "versus",
            " vs ",
            "which is better",
        ]

        if any(
            pattern in q
            for pattern in comparison_patterns
        ):
            return "property_comparison"

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        search_patterns = [
            "show me",
            "find me",
            "search",
            "properties in",
            "properties under",
            "properties below",
            "properties above",
            "bedroom",
        ]

        if any(
            pattern in q
            for pattern in search_patterns
        ):
            return "property_search"

        return "property_general"

    # =========================================================
    # CONTEXT
    # =========================================================

    def build_context(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        return {
            "property": result.get(
                "property",
                {},
            ),
            "location": result.get(
                "location",
                {},
            ),
            "infrastructure": result.get(
                "infrastructure",
                {},
            ),
            "comparables": result.get(
                "comparables",
                {},
            ),
            "valuation": result.get(
                "valuation",
                {},
            ),
            "growth": result.get(
                "growth",
                {},
            ),
            "risk": result.get(
                "risk",
                {},
            ),
            "investment": result.get(
                "investment",
                {},
            ),
            "personalization": result.get(
                "personalization",
                {},
            ),
            "deal": result.get(
                "deal",
                {},
            ),
            "intelligence": result.get(
                "intelligence",
                {},
            ),
            "confidence": result.get(
                "confidence"
            ),
        }

    # =========================================================
    # EVIDENCE
    # =========================================================

    def build_evidence_summary(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:

        property_data = context.get(
            "property",
            {},
        )

        infrastructure = context.get(
            "infrastructure",
            {},
        )

        comparables = context.get(
            "comparables",
            {},
        )

        valuation = context.get(
            "valuation",
            {},
        )

        growth = context.get(
            "growth",
            {},
        )

        risk = context.get(
            "risk",
            {},
        )

        investment = context.get(
            "investment",
            {},
        )

        deal = context.get(
            "deal",
            {},
        )

        metrics = comparables.get(
            "metrics",
            {},
        )

        return {
            "property": {
                "id": property_data.get("id"),
                "title": property_data.get("title"),
                "project_name": property_data.get(
                    "project_name"
                ),
                "developer": property_data.get(
                    "developer"
                ),
                "city": property_data.get(
                    "city"
                ),
                "country": property_data.get(
                    "country"
                ),
                "location": property_data.get(
                    "location"
                ),
                "price": property_data.get(
                    "price"
                ),
                "currency": property_data.get(
                    "currency"
                ),
                "area": property_data.get(
                    "area"
                ),
                "area_unit": property_data.get(
                    "area_unit"
                ),
            },

            "infrastructure": {
                "score": infrastructure.get(
                    "score"
                ),
                "confidence": infrastructure.get(
                    "confidence"
                ),
            },

            "comparables": {
                "count": comparables.get(
                    "count",
                    0,
                ),
                "median_price": metrics.get(
                    "median_price"
                ),
                "average_price": metrics.get(
                    "average_price"
                ),
                "average_price_per_area": metrics.get(
                    "average_price_per_area"
                ),
                "price_range": metrics.get(
                    "price_range"
                ),
            },

            "valuation": valuation,

            "growth": {
                "score": growth.get(
                    "score"
                ),
                "assessment": growth.get(
                    "assessment"
                ),
            },

            "risk": {
                "score": risk.get(
                    "score"
                ),
                "risk_level": risk.get(
                    "risk_level"
                ),
                "reasons": risk.get(
                    "reasons",
                    [],
                ),
                "risks": risk.get(
                    "risks",
                    [],
                ),
            },

            "investment": {
                "score": investment.get(
                    "score"
                ),
                "decision": investment.get(
                    "decision"
                ),
                "assessment": investment.get(
                    "assessment"
                ),
            },

            "deal": {
                "available": deal.get(
                    "available"
                ),
                "deal_score": deal.get(
                    "deal_score"
                ),
                "decision": deal.get(
                    "decision"
                ),
                "confidence": deal.get(
                    "confidence"
                ),
                "reasons": deal.get(
                    "reasons",
                    [],
                ),
                "risks": deal.get(
                    "risks",
                    [],
                ),
            },
        }

    # =========================================================
    # PROMPT
    # =========================================================

    def build_prompt(
        self,
        query: str,
        intent: str,
        context: dict[str, Any],
    ) -> str:

        evidence = self.build_evidence_summary(
            context
        )

        return f"""
USER QUESTION:
{query}

USER INTENT:
{intent}

VERIFIED PROPERTY INTELLIGENCE:
{json.dumps(
    evidence,
    ensure_ascii=False,
    indent=2,
)}

TASK:

Answer the user's question directly.

Use ONLY the verified information above.

Do not invent anything.

Do not explain your reasoning.

Do not mention this prompt.

Do not mention JSON.

Do not mention "the user asks".

Do not mention "we are given".

Do not expose internal reasoning.

Return only the final answer that should be shown in the UI.
""".strip()

    # =========================================================
    # ANSWER
    # =========================================================

    def answer(
        self,
        query: str,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        intent = self.classify_intent(
            query
        )

        context = self.build_context(
            result
        )

        evidence = self.build_evidence_summary(
            context
        )

        # -----------------------------------------------------
        # Deterministic answers
        #
        # These NEVER need Ollama.
        # -----------------------------------------------------

        direct_answer = self.build_direct_answer(
            query=query,
            evidence=evidence,
            intent=intent,
        )

        if direct_answer is not None:

            return {
                "intent": intent,
                "answer": direct_answer,
                "model": "deterministic",
                "guardrails": {
                    "passed": True,
                    "fallback_used": False,
                    "violations": [],
                },
            }

        # -----------------------------------------------------
        # LLM only for questions that really need explanation.
        # -----------------------------------------------------

        prompt = self.build_prompt(
            query=query,
            intent=intent,
            context=context,
        )

        raw_response = self.llm.generate(
            system=self.SYSTEM_PROMPT,
            prompt=prompt,
        )

        cleaned_response = self._clean_response(
            raw_response
        )

        # -----------------------------------------------------
        # Prevent obvious reasoning leakage.
        # -----------------------------------------------------

        if self._looks_like_reasoning(
            cleaned_response
        ):
            cleaned_response = (
                self._extract_final_answer(
                    cleaned_response
                )
            )

        guardrail_result = self.guardrails.validate(
            answer=cleaned_response,
            evidence=evidence,
        )

        return {
            "intent": intent,
            "answer": guardrail_result["answer"],
            "model": "qwen3:4b",
            "guardrails": {
                "passed": guardrail_result.get(
                    "valid",
                    False,
                ),
                "fallback_used": guardrail_result.get(
                    "fallback_used",
                    False,
                ),
                "violations": guardrail_result.get(
                    "violations",
                    [],
                ),
            },
        }

    # =========================================================
    # DIRECT ANSWERS
    # =========================================================

    @staticmethod
    def build_direct_answer(
        query: str,
        evidence: dict[str, Any],
        intent: str,
    ) -> str | None:

        property_data = evidence.get(
            "property",
            {},
        )

        risk = evidence.get(
            "risk",
            {},
        )

        deal = evidence.get(
            "deal",
            {},
        )

        growth = evidence.get(
            "growth",
            {},
        )

        investment = evidence.get(
            "investment",
            {},
        )

        # =====================================================
        # DEVELOPER
        # =====================================================

        if intent == "property_developer":

            developer = property_data.get(
                "developer"
            )

            if developer:
                return (
                    f"The developer is {developer}."
                )

            return (
                "The developer is not available "
                "in the supplied property data."
            )

        # =====================================================
        # PRICE
        # =====================================================

        if intent == "property_price":

            price = property_data.get(
                "price"
            )

            currency = property_data.get(
                "currency"
            )

            if price is not None:

                try:
                    formatted_price = (
                        f"{float(price):,.0f}"
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    formatted_price = str(
                        price
                    )

                if currency:
                    return (
                        f"The asking price is "
                        f"{currency} "
                        f"{formatted_price}."
                    )

                return (
                    f"The asking price is "
                    f"{formatted_price}."
                )

            return (
                "The asking price is not available "
                "in the supplied property data."
            )

        # =====================================================
        # AREA
        # =====================================================

        if intent == "property_area":

            area = property_data.get(
                "area"
            )

            unit = property_data.get(
                "area_unit"
            )

            if area is not None:

                if unit:
                    return (
                        f"The property area is "
                        f"{area} {unit}."
                    )

                return (
                    f"The property area is "
                    f"{area}."
                )

            return (
                "The property area is not available "
                "in the supplied property data."
            )

        # =====================================================
        # LOCATION
        # =====================================================

        if intent == "property_location":

            location = property_data.get(
                "location"
            )

            city = property_data.get(
                "city"
            )

            country = property_data.get(
                "country"
            )

            if location:

                return (
                    f"The property is located in "
                    f"{location}."
                )

            location_parts = [
                value
                for value in [
                    city,
                    country,
                ]
                if value
            ]

            if location_parts:

                return (
                    "The property is located in "
                    + ", ".join(
                        location_parts
                    )
                    + "."
                )

            return (
                "The property location is not available "
                "in the supplied property data."
            )

        # =====================================================
        # RISK
        # =====================================================

        if intent == "property_risk_analysis":

            return (
                AIOrchestrator._build_risk_answer(
                    risk
                )
            )

        # =====================================================
        # INVESTMENT
        # =====================================================

        if intent == "property_investment_analysis":

            return (
                AIOrchestrator._build_investment_answer(
                    deal=deal,
                    growth=growth,
                    risk=risk,
                    investment=investment,
                )
            )

        return None

    # =========================================================
    # RISK ANSWER
    # =========================================================

    @staticmethod
    def _build_risk_answer(
        risk: dict[str, Any],
    ) -> str:

        risk_level = risk.get(
            "risk_level"
        )

        risk_score = risk.get(
            "score"
        )

        risks = risk.get(
            "risks",
            [],
        )

        reasons = risk.get(
            "reasons",
            [],
        )

        lines: list[str] = []

        # -----------------------------------------------------
        # Risk assessment
        # -----------------------------------------------------

        if risk_level:

            if risk_score is not None:

                try:
                    score_text = (
                        f"{float(risk_score):.0f}/100"
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    score_text = str(
                        risk_score
                    )

                lines.append(
                    "The property has a "
                    f"{str(risk_level).lower()} "
                    f"risk level with a Risk Score "
                    f"of {score_text}."
                )

            else:

                lines.append(
                    "The property has a "
                    f"{str(risk_level).lower()} "
                    "risk level."
                )

        elif risk_score is not None:

            try:
                score_text = (
                    f"{float(risk_score):.0f}/100"
                )
            except (
                TypeError,
                ValueError,
            ):
                score_text = str(
                    risk_score
                )

            lines.append(
                f"The Risk Score is {score_text}."
            )

        # -----------------------------------------------------
        # Specific risks
        # -----------------------------------------------------

        all_risks: list[str] = []

        for item in reasons + risks:

            if not item:
                continue

            text = str(item).strip()

            if text and text not in all_risks:
                all_risks.append(text)

        if all_risks:

            lines.append("")
            lines.append("Key risks:")

            for item in all_risks:
                lines.append(
                    f"- {item}"
                )

        # -----------------------------------------------------
        # No risk information
        # -----------------------------------------------------

        if not lines:

            return (
                "A specific risk assessment is not "
                "available in the supplied property data."
            )

        return "\n".join(lines)

    # =========================================================
    # INVESTMENT ANSWER
    # =========================================================

    @staticmethod
    def _build_investment_answer(
        deal: dict[str, Any],
        growth: dict[str, Any],
        risk: dict[str, Any],
        investment: dict[str, Any],
    ) -> str:

        lines: list[str] = []

        deal_decision = deal.get(
            "decision"
        )

        deal_score = deal.get(
            "deal_score"
        )

        investment_decision = investment.get(
            "decision"
        )

        investment_score = investment.get(
            "score"
        )

        growth_score = growth.get(
            "score"
        )

        growth_assessment = growth.get(
            "assessment"
        )

        risk_level = risk.get(
            "risk_level"
        )

        risk_score = risk.get(
            "score"
        )

        reasons = deal.get(
            "reasons",
            [],
        )

        deal_risks = deal.get(
            "risks",
            [],
        )

        risk_items = risk.get(
            "risks",
            [],
        )

        # -----------------------------------------------------
        # Assessment
        # -----------------------------------------------------

        decision = (
            deal_decision
            or investment_decision
        )

        if decision:

            assessment = (
                "The available intelligence suggests "
                f"this is a {str(decision).lower()} "
                "investment opportunity."
            )

        else:

            assessment = (
                "The available intelligence provides "
                "a partial investment assessment."
            )

        if deal_score is not None:

            try:
                score_text = (
                    f"{float(deal_score):.2f}/100"
                )
            except (
                TypeError,
                ValueError,
            ):
                score_text = str(
                    deal_score
                )

            assessment += (
                f" The Deal Score is {score_text}."
            )

        elif investment_score is not None:

            try:
                score_text = (
                    f"{float(investment_score):.0f}/100"
                )
            except (
                TypeError,
                ValueError,
            ):
                score_text = str(
                    investment_score
                )

            assessment += (
                f" The Investment Score is "
                f"{score_text}."
            )

        lines.append(
            assessment
        )

        # -----------------------------------------------------
        # Positives
        # -----------------------------------------------------

        positive_items: list[str] = []

        for item in reasons:

            if item:
                text = str(item).strip()

                if text and text not in positive_items:
                    positive_items.append(text)

        if growth_assessment:

            if str(
                growth_assessment
            ).lower() in {
                "positive",
                "strong",
                "good",
                "favorable",
                "favourable",
            }:

                if (
                    growth_score is not None
                ):

                    positive_items.append(
                        "Growth evidence is "
                        f"{growth_assessment} with a "
                        f"Growth Score of "
                        f"{float(growth_score):.0f}/100."
                    )

                else:

                    positive_items.append(
                        "Growth evidence is "
                        f"{growth_assessment}."
                    )

        if positive_items:

            lines.append("")
            lines.append("Main positives:")

            for item in positive_items[:5]:

                lines.append(
                    f"- {item}"
                )

        # -----------------------------------------------------
        # Concerns
        # -----------------------------------------------------

        concerns: list[str] = []

        for item in deal_risks + risk_items:

            if not item:
                continue

            text = str(item).strip()

            if text and text not in concerns:
                concerns.append(text)

        if risk_level:

            risk_text = (
                f"Overall risk level is "
                f"{str(risk_level).lower()}"
            )

            if risk_score is not None:

                risk_text += (
                    f" with a Risk Score of "
                    f"{float(risk_score):.0f}/100"
                )

            risk_text += "."

            if risk_text not in concerns:
                concerns.insert(
                    0,
                    risk_text,
                )

        if concerns:

            lines.append("")
            lines.append("Main concerns:")

            for item in concerns[:6]:

                lines.append(
                    f"- {item}"
                )

        # -----------------------------------------------------
        # Recommendation wording
        # -----------------------------------------------------

        lines.append("")
        lines.append(
            "Based on the available data, this property "
            "should be reviewed with appropriate due "
            "diligence before making a purchase decision."
        )

        return "\n".join(lines)

    # =========================================================
    # RESPONSE CLEANING
    # =========================================================

    @staticmethod
    def _clean_response(
        response: str,
    ) -> str:

        if not response:
            return ""

        text = response.strip()

        # Remove Qwen reasoning blocks.
        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove markdown fences.
        text = re.sub(
            r"^```(?:text|markdown)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        )

        return text.strip()

    # =========================================================
    # REASONING LEAK DETECTION
    # =========================================================

    @staticmethod
    def _looks_like_reasoning(
        text: str,
    ) -> bool:

        if not text:
            return False

        reasoning_patterns = [
            r"\bwe are given\b",
            r"\bthe user asks\b",
            r"\bthe question type is\b",
            r"\bwe must\b",
            r"\bthe instructions say\b",
            r"\blet's extract\b",
            r"\bsteps:\b",
            r"\bstep\s+\d+",
            r"\btherefore\b.*\bwe\b",
            r"\bwe need to\b",
            r"\bthe response instruction\b",
        ]

        for pattern in reasoning_patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.DOTALL,
            ):
                return True

        return False

    # =========================================================
    # EXTRACT FINAL ANSWER FROM BAD LLM RESPONSE
    # =========================================================

    @staticmethod
    def _extract_final_answer(
        text: str,
    ) -> str:

        if not text:
            return ""

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        # Look for a final direct answer.
        for line in reversed(lines):

            if (
                line.startswith('"')
                and line.endswith('"')
            ):

                return line.strip('"')

            if line.startswith(
                "The "
            ):

                return line

        # If no clean sentence can be extracted,
        # return the original cleaned response.
        return text.strip()


# =============================================================
# MODULE-LEVEL INSTANCE
# =============================================================

ai_orchestrator = AIOrchestrator()
