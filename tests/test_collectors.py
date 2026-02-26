"""Tests for collectors."""
from datetime import datetime

import pytest

from app.collectors.australia import AustraliaCollector
from app.collectors.base import ComplianceChangeData
from app.collectors.european_union import EuropeanUnionCollector
from app.collectors.international import InternationalCollector
from app.collectors.united_kingdom import UnitedKingdomCollector
from app.collectors.united_states import UnitedStatesCollector


def test_australia_collector_sources():
    """Test that Australia collector has valid sources."""
    collector = AustraliaCollector()
    sources = collector.get_sources()

    assert len(sources) > 0
    assert all("url" in source for source in sources)
    assert all("name" in source for source in sources)
    assert all("type" in source for source in sources)


def test_australia_collector_collect():
    """Test that Australia collector returns valid data."""
    collector = AustraliaCollector()
    changes = collector.collect()

    assert isinstance(changes, list)
    if changes:
        change = changes[0]
        assert isinstance(change, ComplianceChangeData)
        assert change.country_code == "AU"
        assert change.jurisdiction == "Australia"
        assert len(change.evidence_text) > 0
        assert len(change.get_evidence_hash()) == 64  # SHA-256


def test_eu_collector_sources():
    """Test that EU collector has valid sources."""
    collector = EuropeanUnionCollector()
    sources = collector.get_sources()

    assert len(sources) > 0
    assert all("url" in source for source in sources)


def test_eu_collector_collect():
    """Test that EU collector returns valid data."""
    collector = EuropeanUnionCollector()
    changes = collector.collect()

    assert isinstance(changes, list)
    if changes:
        change = changes[0]
        assert change.country_code == "EU"
        assert change.jurisdiction == "European Union"


def test_uk_collector_sources():
    """Test that UK collector has valid sources."""
    collector = UnitedKingdomCollector()
    sources = collector.get_sources()

    assert len(sources) > 0


def test_uk_collector_collect():
    """Test that UK collector returns valid data."""
    collector = UnitedKingdomCollector()
    changes = collector.collect()

    assert isinstance(changes, list)
    if changes:
        change = changes[0]
        assert change.country_code == "UK"
        assert change.jurisdiction == "United Kingdom"


def test_us_collector_sources():
    """Test that US collector has valid sources."""
    collector = UnitedStatesCollector()
    sources = collector.get_sources()

    assert len(sources) > 0


def test_us_collector_collect():
    """Test that US collector returns valid data."""
    collector = UnitedStatesCollector()
    changes = collector.collect()

    assert isinstance(changes, list)
    if changes:
        change = changes[0]
        assert change.country_code == "US"
        assert change.jurisdiction == "United States"


def test_international_collector_sources():
    """Test that international collector has valid sources."""
    collector = InternationalCollector()
    sources = collector.get_sources()

    assert len(sources) > 0


def test_international_collector_collect():
    """Test that international collector returns valid data."""
    collector = InternationalCollector()
    changes = collector.collect()

    assert isinstance(changes, list)
    if changes:
        change = changes[0]
        assert change.country_code == "INTL"
        assert change.jurisdiction == "International"


def test_compliance_change_data_hash():
    """Test that evidence hash is generated correctly."""
    data = ComplianceChangeData(
        jurisdiction="Test",
        country_code="TEST",
        legal_domain="test",
        change_type="GUIDANCE",
        title="Test",
        summary="Test",
        source_url="https://example.com",
        publisher="Test",
        published_date=datetime.now(),
        effective_date=None,
        evidence_text="This is test evidence",
    )

    hash1 = data.get_evidence_hash()
    hash2 = data.get_evidence_hash()

    # Same data should produce same hash
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 produces 64-char hex string


def test_compliance_change_data_hash_uniqueness():
    """Test that different evidence produces different hashes."""
    data1 = ComplianceChangeData(
        jurisdiction="Test",
        country_code="TEST",
        legal_domain="test",
        change_type="GUIDANCE",
        title="Test",
        summary="Test",
        source_url="https://example.com",
        publisher="Test",
        published_date=datetime.now(),
        effective_date=None,
        evidence_text="Evidence A",
    )

    data2 = ComplianceChangeData(
        jurisdiction="Test",
        country_code="TEST",
        legal_domain="test",
        change_type="GUIDANCE",
        title="Test",
        summary="Test",
        source_url="https://example.com",
        publisher="Test",
        published_date=datetime.now(),
        effective_date=None,
        evidence_text="Evidence B",
    )

    assert data1.get_evidence_hash() != data2.get_evidence_hash()
