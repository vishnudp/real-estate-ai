from __future__ import annotations

import re
from typing import Any


class AIGuardrails:
    """
    Validates LLM answers against verified property intelligence.

    The guardrails are intentionally conservative:
    - They prevent unsupported numerical claims.
    - They remove accidental LLM reasoning/instruction leakage.
    - They ensure the standard disclaimer is present for analytical answers.
    - They provide a deterministic fallback when the LLM response is invalid.
    """

    DISCLAIMER = (
        "This is an indicative analysis based on available property "
        "data and POC-generated intelligence. It is not financial "
        "advice or a professional property valuation."
    )

    REQUIRED_SECTIONS = [
        "Assessment:",
        "Why:",
        "Main concerns:",
        "Valuation:",
        "Confidence:",
    ]

    FORBIDDEN_PATTERNS = [
        r"\bwe are given\b",
        r"\bthe user asks\b",
        r"\buser question\b",
        r"\bquestion type\b",
        r"\blet's analyze\b",
        r"\blet us analyze\b",
        r"\bwe must\b",
        r"\bwe need to\b",
        r"\bthe instructions\b",
        r"\bresponse instruction\b",
        r"\boutput must be\b",
        r"\bsteps?:\b",
        r"\bfrom the verified\b",
        r"\bimportant:\b",
        r"\bhowever, note\b",
        r"\binternal reasoning\b",
        r"\bchain of thought\b",
        r"\bjson\b",
    ]

    def __init__(self) -> None:
        pass

    # =========================================================
    # PUBLIC CLEAN
    # =========================================================

    @classmethod
    def clean(
        cls,
        answer: str,
    ) -> str:
        """
        Clean accidental model reasoning and formatting noise.
        """

        if not answer:
            return ""

        text = str(answer).strip()

        # Remove Qwen thinking blocks.
        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove incomplete thinking tags.
        text = re.sub(
            r"<think>.*$",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

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

        # Remove common accidental prefixes.
        text = re.sub(
            r"^(answer|response)\s*:\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # Collapse excessive blank lines.
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    # =========================================================
    # NUMBER EXTRACTION
    # =========================================================

    @classmethod
    def _extract_numbers(
        cls,
        value: Any,
    ) -> set[str]:
        """
        Extract normalized numbers from arbitrary evidence.
        """

        allowed: set[str] = set()

        def walk(item: Any) -> None:

            if isinstance(item, dict):

                for child in item.values():
                    walk(child)

            elif isinstance(item, list):

                for child in item:
                    walk(child)

            elif isinstance(item, (int, float)):

                allowed.add(
                    cls._normalize_number(
                        str(item)
                    )
                )

            elif isinstance(item, str):

                numbers = re.findall(
                    r"-?\d+(?:,\d{3})*(?:\.\d+)?%?",
                    item,
                )

                for number in numbers:

                    allowed.add(
                        cls._normalize_number(
                            number
                        )
                    )

        walk(value)

        return allowed

    # =========================================================
    # NUMBER NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize_number(
        value: str,
    ) -> str:

        value = str(value).strip()
        value = value.replace(",", "")

        is_percent = value.endswith("%")

        if is_percent:
            value = value[:-1]

        try:

            number = float(value)

            normalized = (
                f"{number:.10f}"
                .rstrip("0")
                .rstrip(".")
            )

            if normalized == "-0":
                normalized = "0"

            if is_percent:
                return f"{normalized}%"

            return normalized

        except (ValueError, TypeError):

            return value

    # =========================================================
    # NUMBER VALIDATION
    # =========================================================

    @classmethod
    def _validate_numbers(
        cls,
        answer: str,
        evidence: dict[str, Any],
    ) -> list[str]:
        """
        Detect numerical values appearing in the answer that
        do not exist in the verified evidence.

        This deliberately ignores:
        - list numbering
        - section numbering
        - years in ordinary text when they are not evidence claims

        The method returns violation strings.
        """

        violations: list[str] = []

        allowed = cls._extract_numbers(
            evidence
        )

        # Match integers, decimals, percentages and comma-formatted
        # numbers.
        numbers = re.findall(
            r"-?\d+(?:,\d{3})*(?:\.\d+)?%?",
            answer,
        )

        for number in numbers:

            normalized = cls._normalize_number(
                number
            )

            # Ignore simple list markers such as "1.".
            # They should not be treated as factual numbers.
            if normalized in {"1", "2", "3", "4", "5"}:

                pattern = rf"^\s*{re.escape(number)}[.)]\s+"

                if re.search(
                    pattern,
                    answer,
                    flags=re.MULTILINE,
                ):
                    continue

            if normalized not in allowed:

                violations.append(
                    f"unsupported_number:{number}"
                )

        return list(dict.fromkeys(violations))

    # =========================================================
    # FORBIDDEN CONTENT VALIDATION
    # =========================================================

    @classmethod
    def _validate_forbidden_content(
        cls,
        answer: str,
    ) -> list[str]:

        violations: list[str] = []

        for pattern in cls.FORBIDDEN_PATTERNS:

            if re.search(
                pattern,
                answer,
                flags=re.IGNORECASE,
            ):

                violations.append(
                    f"forbidden_content:{pattern}"
                )

        return violations

    # =========================================================
    # DISCLAIMER VALIDATION
    # =========================================================

    @classmethod
    def _has_disclaimer(
        cls,
        answer: str,
    ) -> bool:

        normalized_answer = re.sub(
            r"\s+",
            " ",
            answer.strip().lower(),
        )

        normalized_disclaimer = re.sub(
            r"\s+",
            " ",
            cls.DISCLAIMER.strip().lower(),
        )

        return (
            normalized_disclaimer
            in normalized_answer
        )

    # =========================================================
    # REQUIRED SECTION VALIDATION
    # =========================================================

    @classmethod
    def _validate_sections(
        cls,
        answer: str,
    ) -> list[str]:

        violations: list[str] = []

        for section in cls.REQUIRED_SECTIONS:

            if section.lower() not in answer.lower():

                violations.append(
                    f"missing_section:{section[:-1]}"
                )

        return violations

    # =========================================================
    # FALLBACK VALUATION
    # =========================================================

    @staticmethod
    def _build_valuation_text(
        valuation: dict[str, Any],
        property_data: dict[str, Any],
    ) -> str:

        if not valuation.get("available"):

            return (
                "A deterministic valuation is not available "
                "from the supplied property data."
            )

        estimated_value = valuation.get(
            "estimated_value"
        )

        upside = valuation.get(
            "upside_percent"
        )

        asking_price = property_data.get(
            "price"
        )

        currency = (
            property_data.get("currency")
            or ""
        )

        if (
            estimated_value is not None
            and upside is not None
            and asking_price is not None
        ):

            try:

                estimated_display = (
                    f"{currency}"
                    f"{estimated_value / 1_000_000:.2f}M"
                )

                asking_display = (
                    f"{currency}"
                    f"{asking_price / 1_000_000:.2f}M"
                )

                if upside < 0:

                    return (
                        f"The estimated value is approximately "
                        f"{estimated_display} versus an asking "
                        f"price of {asking_display}. This indicates "
                        f"the property is approximately "
                        f"{abs(upside):.2f}% above its estimated "
                        f"value."
                    )

                if upside > 0:

                    return (
                        f"The estimated value is approximately "
                        f"{estimated_display} versus an asking "
                        f"price of {asking_display}. This indicates "
                        f"approximately {upside:.2f}% upside relative "
                        f"to its estimated value."
                    )

                return (
                    f"The estimated value is approximately "
                    f"{estimated_display}, which is approximately "
                    f"aligned with the asking price of "
                    f"{asking_display}."
                )

            except (TypeError, ValueError):

                pass

        if (
            estimated_value is not None
            and upside is not None
        ):

            return (
                f"The estimated value is approximately "
                f"{estimated_value:,.2f}. The supplied valuation "
                f"indicates approximately "
                f"{upside:.2f}% upside relative to the "
                f"estimated value."
            )

        return (
            "A valuation is available, but some valuation "
            "details are unavailable."
        )

    # =========================================================
    # FALLBACK
    # =========================================================

    def build_fallback(
        self,
        evidence: dict[str, Any],
    ) -> str:

        property_data = evidence.get(
            "property",
            {},
        )

        deal = evidence.get(
            "deal",
            {},
        )

        valuation = evidence.get(
            "valuation",
            {},
        )

        growth = evidence.get(
            "growth",
            {},
        )

        risk = evidence.get(
            "risk",
            {},
        )

        investment = evidence.get(
            "investment",
            {},
        )

        deal_decision = (
            deal.get("decision")
            or "unavailable"
        )

        deal_score = deal.get(
            "deal_score"
        )

        reasons = deal.get(
            "reasons",
            [],
        )

        risks = deal.get(
            "risks",
            [],
        )

        risk_level = risk.get(
            "risk_level"
        )

        risk_score = risk.get(
            "score"
        )

        risk_reasons = risk.get(
            "reasons",
            [],
        )

        risk_risks = risk.get(
            "risks",
            [],
        )

        growth_score = growth.get(
            "score"
        )

        investment_score = investment.get(
            "score"
        )

        valuation_text = (
            self._build_valuation_text(
                valuation,
                property_data,
            )
        )

        # -----------------------------------------------------
        # Assessment
        # -----------------------------------------------------

        assessment_parts: list[str] = []

        if deal_decision != "unavailable":

            assessment_parts.append(
                f"This property appears to be a "
                f"{deal_decision} investment opportunity "
                f"based on the current intelligence."
            )

        else:

            assessment_parts.append(
                "The available property intelligence "
                "does not provide a complete investment assessment."
            )

        if deal_score is not None:

            try:

                assessment_parts.append(
                    f"Its Deal Score is "
                    f"{float(deal_score):.2f}/100."
                )

            except (TypeError, ValueError):
                pass

        assessment = " ".join(
            assessment_parts
        )

        # -----------------------------------------------------
        # Why
        # -----------------------------------------------------

        why_lines: list[str] = []

        for reason in reasons:

            if reason:
                why_lines.append(
                    f"- {reason}"
                )

        if investment_score is not None:

            try:

                why_lines.append(
                    f"- Investment Score is "
                    f"{float(investment_score):.0f}/100."
                )

            except (TypeError, ValueError):
                pass

        if not why_lines:

            why_lines.append(
                "- No additional evidence-backed reasons "
                "are available."
            )

        # -----------------------------------------------------
        # Main concerns
        # -----------------------------------------------------

        concern_lines: list[str] = []

        combined_risks = []

        for item in risks:
            if item:
                combined_risks.append(item)

        for item in risk_risks:
            if item and item not in combined_risks:
                combined_risks.append(item)

        for item in combined_risks:

            concern_lines.append(
                f"- {item}"
            )

        if risk_level:

            risk_text = (
                f"Risk level is "
                f"{str(risk_level).lower()}"
            )

            if risk_score is not None:

                try:

                    risk_text += (
                        f" with a Risk Score of "
                        f"{float(risk_score):.0f}/100."
                    )

                except (TypeError, ValueError):

                    risk_text += "."

            else:

                risk_text += "."

            already_present = any(
                "risk level" in line.lower()
                for line in concern_lines
            )

            if not already_present:

                concern_lines.insert(
                    0,
                    f"- {risk_text}",
                )

        for item in risk_reasons:

            if (
                item
                and item not in combined_risks
                and not any(
                    item.lower() in line.lower()
                    for line in concern_lines
                )
            ):

                concern_lines.append(
                    f"- {item}"
                )

        if growth_score is not None:

            growth_line_exists = any(
                "growth score" in line.lower()
                for line in concern_lines
            )

            if not growth_line_exists:

                try:

                    concern_lines.append(
                        f"- Growth Score is "
                        f"{float(growth_score):.0f}/100."
                    )

                except (TypeError, ValueError):
                    pass

        if not concern_lines:

            concern_lines.append(
                "- No additional evidence-backed concerns "
                "are available."
            )

        # -----------------------------------------------------
        # Confidence
        # -----------------------------------------------------

        confidence = (
            "The assessment is based on the available "
            "property and market intelligence."
        )

        # -----------------------------------------------------
        # Final answer
        # -----------------------------------------------------

        return "\n".join(
            [
                "Assessment:",
                assessment,
                "",
                "Why:",
                *why_lines,
                "",
                "Main concerns:",
                *concern_lines,
                "",
                "Valuation:",
                valuation_text,
                "",
                "Confidence:",
                confidence,
                "",
                self.DISCLAIMER,
            ]
        )

    # =========================================================
    # FALLBACK VALIDATION
    # =========================================================

    def _validate_fallback(
        self,
        fallback: str,
        evidence: dict[str, Any],
    ) -> list[str]:

        violations: list[str] = []

        # Required sections.
        violations.extend(
            self._validate_sections(
                fallback
            )
        )

        # Forbidden content.
        violations.extend(
            self._validate_forbidden_content(
                fallback
            )
        )

        # Numbers in the deterministic fallback must also
        # originate from evidence.
        violations.extend(
            self._validate_numbers(
                fallback,
                evidence,
            )
        )

        # Disclaimer should always be present.
        if not self._has_disclaimer(
            fallback
        ):

            violations.append(
                "missing_disclaimer"
            )

        return list(
            dict.fromkeys(violations)
        )

    # =========================================================
    # ANALYTICAL ANSWER VALIDATION
    # =========================================================

    def _validate_answer(
        self,
        answer: str,
        evidence: dict[str, Any],
    ) -> list[str]:

        violations: list[str] = []

        if not answer.strip():

            violations.append(
                "empty_answer"
            )

            return violations

        violations.extend(
            self._validate_forbidden_content(
                answer
            )
        )

        violations.extend(
            self._validate_numbers(
                answer,
                evidence,
            )
        )

        return list(
            dict.fromkeys(violations)
        )

    # =========================================================
    # PUBLIC VALIDATE
    # =========================================================

    def validate(
        self,
        answer: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate an AI response.

        Returns:
            {
                "valid": bool,
                "answer": str,
                "fallback_used": bool,
                "violations": list[str],
            }
        """

        cleaned = self.clean(
            answer
        )

        violations = self._validate_answer(
            cleaned,
            evidence,
        )

        # -----------------------------------------------------
        # Valid response
        # -----------------------------------------------------

        if not violations:

            return {
                "valid": True,
                "answer": cleaned,
                "fallback_used": False,
                "violations": [],
            }

        # -----------------------------------------------------
        # Invalid LLM response
        # -----------------------------------------------------

        fallback = self.build_fallback(
            evidence
        )

        fallback_violations = (
            self._validate_fallback(
                fallback,
                evidence,
            )
        )

        # The deterministic fallback is authoritative.
        # Even if its own numerical validation reports a
        # problem, return it rather than returning model
        # reasoning/instructions to the user.
        return {
            "valid": False,
            "answer": fallback,
            "fallback_used": True,
            "violations": list(
                dict.fromkeys(
                    violations
                    + fallback_violations
                )
            ),
        }
