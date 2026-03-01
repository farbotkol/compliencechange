"""International organizations compliance collector."""
from datetime import datetime

from app.collectors.base import BaseCollector, ComplianceChangeData


class InternationalCollector(BaseCollector):
    """Collector for international organization compliance changes."""

    def get_sources(self) -> list[dict]:
        """Get international organization sources."""
        return [
            {
                "url": "https://www.ilo.org/global/about-the-ilo/newsroom/lang--en/index.htm",
                "name": "International Labour Organization",
                "type": "employment_law",
            },
            {
                "url": "https://www.oecd.org/tax/",
                "name": "OECD",
                "type": "tax",
            },
        ]

    def collect(self) -> list[ComplianceChangeData]:
        """
        Collect international compliance changes.

        Note: This is a demonstration implementation.
        """
        changes = []

        # Example ILO guidance
        change = ComplianceChangeData(
            jurisdiction="International",
            country_code="INTL",
            legal_domain="employment_law",
            change_type="GUIDANCE",
            title="ILO publishes guidance on platform work and employment relationships",
            summary=(
                "The International Labour Organization has published new guidance on "
                "employment relationships in the platform economy. This provides "
                "international context for contractor classification issues globally."
            ),
            source_url="https://www.ilo.org/global/topics/employment-relationship/lang--en/index.htm",
            publisher="International Labour Organization",
            published_date=datetime(2024, 1, 10),
            effective_date=None,
            evidence_text=(
                "ILO Guidance: Countries should ensure that relevant laws and regulations "
                "guarantee appropriate protection to workers in an employment relationship, "
                "including those in atypical or new forms of contractual arrangements."
            ),
        )
        changes.append(change)

        return changes
