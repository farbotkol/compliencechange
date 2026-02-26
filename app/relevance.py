"""Relevance scoring engine for compliance changes."""
import re
from typing import Dict, List

from app.models import ImpactLevel


class RelevanceEngine:
    """Rule-based relevance scoring for CXC compliance changes."""

    # High-impact keywords
    HIGH_IMPACT_KEYWORDS = [
        "contractor",
        "misclassification",
        "employment status",
        "employee classification",
        "worker classification",
        "independent contractor",
        "payroll",
        "withholding",
        "employer of record",
        "eor",
        "aor",
        "agent of record",
        "contractor of record",
        "cross-border",
        "data privacy",
        "gdpr",
        "personal data",
        "tax obligation",
        "social security",
        "employment law",
        "termination",
        "severance",
        "benefits",
        "pension",
    ]

    # Medium-impact keywords
    MEDIUM_IMPACT_KEYWORDS = [
        "labor",
        "labour",
        "wages",
        "minimum wage",
        "working hours",
        "leave",
        "vacation",
        "holiday",
        "reporting",
        "compliance",
        "regulation",
        "employment",
        "workforce",
        "contingent",
        "temporary",
        "contract",
    ]

    # Low-impact keywords
    LOW_IMPACT_KEYWORDS = [
        "guidance",
        "template",
        "form",
        "administrative",
        "procedural",
        "format",
        "documentation",
    ]

    # Service line mappings
    SERVICE_MAPPINGS = {
        "EOR": ["employer of record", "eor", "employment", "payroll"],
        "AOR": ["agent of record", "aor", "contractor"],
        "COR": ["contractor of record", "cor", "independent contractor"],
        "MSP": ["msp", "managed service", "contingent workforce"],
        "Payroll": ["payroll", "withholding", "tax", "social security"],
        "Compliance-as-a-Service": ["compliance", "regulation", "data privacy"],
    }

    @staticmethod
    def calculate_impact(
        title: str, summary: str, change_type: str, legal_domain: str
    ) -> str:
        """
        Calculate impact level based on content analysis.

        Args:
            title: The title of the compliance change
            summary: The summary of the compliance change
            change_type: The type of change (ENACTED_LAW, etc.)
            legal_domain: The legal domain (employment law, etc.)

        Returns:
            Impact level (HIGH, MEDIUM, LOW)
        """
        text = f"{title} {summary}".lower()

        # Check for high-impact keywords
        high_count = sum(
            1
            for keyword in RelevanceEngine.HIGH_IMPACT_KEYWORDS
            if keyword.lower() in text
        )

        # Boost score for enacted laws vs guidance
        type_multiplier = 1.5 if change_type == "ENACTED_LAW" else 1.0

        # Boost score for employment/payroll domains
        domain_boost = 0
        if any(
            domain in legal_domain.lower()
            for domain in ["employment", "payroll", "tax", "contractor"]
        ):
            domain_boost = 1

        # Calculate weighted score
        weighted_high = high_count * type_multiplier + domain_boost

        if weighted_high >= 2:
            return ImpactLevel.HIGH.value

        # Check for medium-impact keywords
        medium_count = sum(
            1
            for keyword in RelevanceEngine.MEDIUM_IMPACT_KEYWORDS
            if keyword.lower() in text
        )

        if medium_count >= 2 or weighted_high >= 1:
            return ImpactLevel.MEDIUM.value

        return ImpactLevel.LOW.value

    @staticmethod
    def identify_services(title: str, summary: str) -> List[str]:
        """
        Identify which CXC service lines are impacted.

        Args:
            title: The title of the compliance change
            summary: The summary of the compliance change

        Returns:
            List of impacted service lines
        """
        text = f"{title} {summary}".lower()
        impacted_services = []

        for service, keywords in RelevanceEngine.SERVICE_MAPPINGS.items():
            if any(keyword.lower() in text for keyword in keywords):
                impacted_services.append(service)

        return impacted_services or ["General"]

    @staticmethod
    def score_change(
        title: str, summary: str, change_type: str, legal_domain: str
    ) -> Dict[str, any]:
        """
        Score a compliance change for relevance.

        Args:
            title: The title of the compliance change
            summary: The summary of the compliance change
            change_type: The type of change
            legal_domain: The legal domain

        Returns:
            Dictionary with impact_level and services
        """
        impact_level = RelevanceEngine.calculate_impact(
            title, summary, change_type, legal_domain
        )
        services = RelevanceEngine.identify_services(title, summary)

        return {
            "impact_level": impact_level,
            "services": services,
            "service_impacted": ", ".join(services),
        }
