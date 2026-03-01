"""Tests for relevance scoring engine."""

from app.models import ImpactLevel
from app.relevance import RelevanceEngine


def test_high_impact_contractor_misclassification():
    """Test that contractor misclassification is scored as high impact."""
    title = "New contractor misclassification penalties"
    summary = "Government introduces strict penalties for independent contractor misclassification"
    change_type = "ENACTED_LAW"
    legal_domain = "employment_law"

    result = RelevanceEngine.score_change(title, summary, change_type, legal_domain)

    assert result["impact_level"] == ImpactLevel.HIGH.value
    assert "COR" in result["services"] or "AOR" in result["services"]


def test_high_impact_payroll_tax():
    """Test that payroll tax changes are scored as high impact."""
    title = "Payroll tax withholding changes"
    summary = "New withholding requirements for employer of record services"
    change_type = "ENACTED_LAW"
    legal_domain = "tax"

    result = RelevanceEngine.score_change(title, summary, change_type, legal_domain)

    assert result["impact_level"] == ImpactLevel.HIGH.value
    assert "Payroll" in result["services"] or "EOR" in result["services"]


def test_medium_impact_wage_update():
    """Test that wage updates are scored as medium impact."""
    title = "Minimum wage increase"
    summary = "Annual adjustment to minimum wage rates for employees"
    change_type = "REGULATORY_UPDATE"
    legal_domain = "employment_law"

    result = RelevanceEngine.score_change(title, summary, change_type, legal_domain)

    assert result["impact_level"] in [ImpactLevel.MEDIUM.value, ImpactLevel.HIGH.value]


def test_low_impact_guidance():
    """Test that administrative guidance is scored as low impact."""
    title = "Updated reporting template"
    summary = "Administrative guidance on new form format for documentation"
    change_type = "GUIDANCE"
    legal_domain = "administrative"

    result = RelevanceEngine.score_change(title, summary, change_type, legal_domain)

    assert result["impact_level"] == ImpactLevel.LOW.value


def test_service_identification_eor():
    """Test that EOR services are correctly identified."""
    title = "Employer of Record compliance requirements"
    summary = "New requirements for EOR service providers regarding payroll"

    services = RelevanceEngine.identify_services(title, summary)

    assert "EOR" in services or "Payroll" in services


def test_service_identification_data_privacy():
    """Test that data privacy affects compliance services."""
    title = "GDPR enforcement update"
    summary = "New guidance on personal data processing and compliance requirements"

    services = RelevanceEngine.identify_services(title, summary)

    assert "Compliance-as-a-Service" in services


def test_enacted_law_boost():
    """Test that enacted laws get priority over guidance."""
    title = "Employment contract requirements"
    summary = "Updates to employment contracts"

    enacted_result = RelevanceEngine.score_change(
        title, summary, "ENACTED_LAW", "employment_law"
    )
    guidance_result = RelevanceEngine.score_change(
        title, summary, "GUIDANCE", "employment_law"
    )

    # Enacted should have equal or higher impact
    impact_order = {ImpactLevel.LOW.value: 0, ImpactLevel.MEDIUM.value: 1, ImpactLevel.HIGH.value: 2}
    assert impact_order[enacted_result["impact_level"]] >= impact_order[guidance_result["impact_level"]]
