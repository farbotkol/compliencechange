"""United Kingdom compliance collector."""
from datetime import datetime
from typing import List

from app.collectors.base import BaseCollector, ComplianceChangeData


class UnitedKingdomCollector(BaseCollector):
    """Collector for UK compliance changes."""

    def get_sources(self) -> List[dict]:
        """Get UK authoritative sources."""
        return [
            {
                "url": "https://www.gov.uk/government/organisations/hm-revenue-customs",
                "name": "HM Revenue & Customs",
                "type": "tax",
            },
            {
                "url": "https://www.gov.uk/government/organisations/department-for-business-and-trade",
                "name": "Department for Business and Trade",
                "type": "employment_law",
            },
        ]

    def collect(self) -> List[ComplianceChangeData]:
        """
        Collect UK compliance changes.

        Note: This is a demonstration implementation.
        """
        changes = []

        # Example IR35 change (relevant to contractor classification)
        change = ComplianceChangeData(
            jurisdiction="United Kingdom",
            country_code="UK",
            legal_domain="tax",
            change_type="REGULATORY_UPDATE",
            title="HMRC updates IR35 guidance for off-payroll working",
            summary=(
                "HM Revenue & Customs has updated its guidance on off-payroll working "
                "rules (IR35). This impacts how contractors are engaged and classified, "
                "directly affecting AOR and contractor management services."
            ),
            source_url="https://www.gov.uk/guidance/understanding-off-payroll-working-ir35",
            publisher="HM Revenue & Customs – UK",
            published_date=datetime(2024, 1, 20),
            effective_date=None,
            evidence_text=(
                "HMRC IR35 guidance: Off-payroll working rules ensure that individuals "
                "who work like employees but through their own limited company pay broadly "
                "the same tax and National Insurance as employees."
            ),
        )
        changes.append(change)

        return changes
