"""Base collector class for compliance monitoring."""
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

import httpx
from bs4 import BeautifulSoup


@dataclass
class ComplianceChangeData:
    """Data class for compliance changes."""

    jurisdiction: str
    country_code: str
    legal_domain: str
    change_type: str
    title: str
    summary: str
    source_url: str
    publisher: str
    published_date: datetime | None
    effective_date: datetime | None
    evidence_text: str

    def get_evidence_hash(self) -> str:
        """Generate SHA-256 hash of evidence text."""
        return hashlib.sha256(self.evidence_text.encode("utf-8")).hexdigest()


class BaseCollector(ABC):
    """Base class for jurisdiction-specific collectors."""

    def __init__(self, timeout: int = 30):
        """
        Initialize collector.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
        self.user_agent = (
            "CXC-Compliance-Monitor/1.0 (Automated compliance monitoring; "
            "contact: compliance@cxc.example.com)"
        )

    @abstractmethod
    def get_sources(self) -> list[dict]:
        """
        Get list of authoritative sources for this jurisdiction.

        Returns:
            List of source dictionaries with 'url', 'name', 'type' keys
        """
        pass

    @abstractmethod
    def collect(self) -> list[ComplianceChangeData]:
        """
        Collect compliance changes from sources.

        Returns:
            List of ComplianceChangeData objects
        """
        pass

    async def fetch_url(self, url: str) -> str | None:
        """
        Fetch content from URL.

        Args:
            url: URL to fetch

        Returns:
            HTML content or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    url, headers={"User-Agent": self.user_agent}, follow_redirects=True
                )
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content.

        Args:
            html: HTML string

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "lxml")

    def extract_text(self, element, max_length: int = 1000) -> str:
        """
        Extract text from HTML element.

        Args:
            element: BeautifulSoup element
            max_length: Maximum text length

        Returns:
            Extracted text
        """
        if element:
            text = element.get_text(strip=True)
            return text[:max_length] if len(text) > max_length else text
        return ""
