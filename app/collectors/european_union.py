"""European Union compliance collector."""
from datetime import datetime
from typing import List

from app.collectors.base import BaseCollector, ComplianceChangeData


class EuropeanUnionCollector(BaseCollector):
    """Collector for EU compliance changes."""

    def get_sources(self) -> List[dict]:
        """Get EU authoritative sources."""
        return [
            {
                "url": "https://ec.europa.eu/social/main.jsp?catId=157&langId=en",
                "name": "European Commission - Employment",
                "type": "employment_law",
            },
            {
                "url": "https://edpb.europa.eu/news/news_en",
                "name": "European Data Protection Board",
                "type": "data_privacy",
            },
        ]

    def collect(self) -> List[ComplianceChangeData]:
        """
        Collect EU compliance changes.

        Note: This is a demonstration implementation.
        """
        changes = []

        # Example GDPR-related change
        change = ComplianceChangeData(
            jurisdiction="European Union",
            country_code="EU",
            legal_domain="data_privacy",
            change_type="REGULATORY_UPDATE",
            title="EDPB adopts guidelines on international data transfers",
            summary=(
                "The European Data Protection Board has adopted new guidelines "
                "regarding international data transfers under GDPR. This affects "
                "cross-border workforce management and data processing for EOR services."
            ),
            source_url="https://edpb.europa.eu/our-work-tools/our-documents/guidelines_en",
            publisher="European Data Protection Board – EU",
            published_date=datetime(2024, 2, 1),
            effective_date=None,
            evidence_text=(
                "EDPB Guidelines: Controllers and processors must ensure appropriate "
                "safeguards when transferring personal data outside the EEA, including "
                "employee and contractor data."
            ),
        )
        changes.append(change)

        return changes
