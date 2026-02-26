"""Tests for database operations and idempotency."""
from datetime import datetime

import pytest

from app.collectors.base import ComplianceChangeData
from app.db import save_compliance_change
from app.models import ComplianceChange


def test_save_compliance_change(db_session):
    """Test saving a compliance change."""
    change_data = ComplianceChangeData(
        jurisdiction="Australia",
        country_code="AU",
        legal_domain="employment_law",
        change_type="ENACTED_LAW",
        title="Test Change",
        summary="Test summary",
        source_url="https://example.com",
        publisher="Test Publisher",
        published_date=datetime(2024, 1, 1),
        effective_date=None,
        evidence_text="Test evidence",
    )

    result = save_compliance_change(db_session, change_data)

    assert result is not None
    assert result.id is not None
    assert result.title == "Test Change"
    assert result.country_code == "AU"
    assert result.impact_level in ["HIGH", "MEDIUM", "LOW"]


def test_idempotency_same_evidence(db_session):
    """Test that same evidence doesn't create duplicates."""
    change_data = ComplianceChangeData(
        jurisdiction="Australia",
        country_code="AU",
        legal_domain="employment_law",
        change_type="ENACTED_LAW",
        title="Test Change",
        summary="Test summary",
        source_url="https://example.com",
        publisher="Test Publisher",
        published_date=datetime(2024, 1, 1),
        effective_date=None,
        evidence_text="Unique evidence text",
    )

    # Save first time
    result1 = save_compliance_change(db_session, change_data)
    assert result1 is not None

    # Save second time with same evidence
    result2 = save_compliance_change(db_session, change_data)
    assert result2 is None  # Should return None (already exists)

    # Verify only one record in database
    count = db_session.query(ComplianceChange).count()
    assert count == 1


def test_different_evidence_creates_new_record(db_session):
    """Test that different evidence creates new records."""
    change_data1 = ComplianceChangeData(
        jurisdiction="Australia",
        country_code="AU",
        legal_domain="employment_law",
        change_type="ENACTED_LAW",
        title="Test Change 1",
        summary="Test summary 1",
        source_url="https://example.com/1",
        publisher="Test Publisher",
        published_date=datetime(2024, 1, 1),
        effective_date=None,
        evidence_text="Evidence text A",
    )

    change_data2 = ComplianceChangeData(
        jurisdiction="Australia",
        country_code="AU",
        legal_domain="employment_law",
        change_type="ENACTED_LAW",
        title="Test Change 2",
        summary="Test summary 2",
        source_url="https://example.com/2",
        publisher="Test Publisher",
        published_date=datetime(2024, 1, 2),
        effective_date=None,
        evidence_text="Evidence text B",
    )

    result1 = save_compliance_change(db_session, change_data1)
    result2 = save_compliance_change(db_session, change_data2)

    assert result1 is not None
    assert result2 is not None
    assert result1.id != result2.id

    count = db_session.query(ComplianceChange).count()
    assert count == 2


def test_impact_level_assigned(db_session):
    """Test that impact level is correctly assigned."""
    change_data = ComplianceChangeData(
        jurisdiction="Australia",
        country_code="AU",
        legal_domain="employment_law",
        change_type="ENACTED_LAW",
        title="Contractor misclassification penalties",
        summary="New penalties for misclassifying independent contractors",
        source_url="https://example.com",
        publisher="Test Publisher",
        published_date=datetime(2024, 1, 1),
        effective_date=None,
        evidence_text="Test evidence about contractor classification",
    )

    result = save_compliance_change(db_session, change_data)

    assert result is not None
    # Should be HIGH impact due to "contractor" and "misclassification" keywords
    assert result.impact_level == "HIGH"


def test_service_impacted_assigned(db_session):
    """Test that service impacted is correctly assigned."""
    change_data = ComplianceChangeData(
        jurisdiction="Australia",
        country_code="AU",
        legal_domain="employment_law",
        change_type="ENACTED_LAW",
        title="Employer of Record compliance requirements",
        summary="New requirements for EOR providers and payroll processing",
        source_url="https://example.com",
        publisher="Test Publisher",
        published_date=datetime(2024, 1, 1),
        effective_date=None,
        evidence_text="Test evidence about EOR and payroll",
    )

    result = save_compliance_change(db_session, change_data)

    assert result is not None
    assert result.service_impacted is not None
    # Should include EOR and/or Payroll
    assert "EOR" in result.service_impacted or "Payroll" in result.service_impacted
