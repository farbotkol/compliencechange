"""Database utilities."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.collectors.base import ComplianceChangeData
from app.models import ComplianceChange, ScanRun, get_engine, get_session_maker
from app.relevance import RelevanceEngine


def get_db_session(database_url: str = "sqlite:///compliance.db") -> Session:
    """Get database session."""
    engine = get_engine(database_url)
    session_maker = get_session_maker(engine)
    return session_maker()


def save_compliance_change(
    session: Session, change_data: ComplianceChangeData
) -> ComplianceChange | None:
    """
    Save compliance change to database (idempotent).

    Args:
        session: Database session
        change_data: ComplianceChangeData object

    Returns:
        ComplianceChange object or None if already exists
    """
    evidence_hash = change_data.get_evidence_hash()

    # Check if already exists
    existing = (
        session.query(ComplianceChange)
        .filter(ComplianceChange.evidence_sha256 == evidence_hash)
        .first()
    )

    if existing:
        return None  # Already exists, idempotent

    # Score the change
    scoring = RelevanceEngine.score_change(
        change_data.title, change_data.summary, change_data.change_type, change_data.legal_domain
    )

    # Create new record
    compliance_change = ComplianceChange(
        jurisdiction=change_data.jurisdiction,
        country_code=change_data.country_code,
        legal_domain=change_data.legal_domain,
        service_impacted=scoring["service_impacted"],
        change_type=change_data.change_type,
        title=change_data.title,
        summary=change_data.summary,
        source_url=change_data.source_url,
        publisher=change_data.publisher,
        published_date=change_data.published_date,
        effective_date=change_data.effective_date,
        retrieved_at=datetime.utcnow(),
        impact_level=scoring["impact_level"],
        evidence_text=change_data.evidence_text,
        evidence_sha256=evidence_hash,
    )

    session.add(compliance_change)
    session.commit()
    session.refresh(compliance_change)

    return compliance_change


def create_scan_run(session: Session) -> ScanRun:
    """Create a new scan run."""
    scan_run = ScanRun(start_time=datetime.utcnow(), status="running")
    session.add(scan_run)
    session.commit()
    session.refresh(scan_run)
    return scan_run


def complete_scan_run(
    session: Session, scan_run_id: int, items_found: int, failures: str | None = None
):
    """Complete a scan run."""
    scan_run = session.query(ScanRun).filter(ScanRun.id == scan_run_id).first()
    if scan_run:
        scan_run.end_time = datetime.utcnow()
        scan_run.items_found = items_found
        scan_run.failures = failures
        scan_run.status = "completed" if not failures else "completed_with_errors"
        session.commit()


def get_latest_changes(
    session: Session, limit: int = 50, country: str | None = None,
    domain: str | None = None, impact: str | None = None
) -> list[ComplianceChange]:
    """Get latest compliance changes with optional filters."""
    query = session.query(ComplianceChange).order_by(ComplianceChange.retrieved_at.desc())

    if country:
        query = query.filter(ComplianceChange.country_code == country)
    if domain:
        query = query.filter(ComplianceChange.legal_domain == domain)
    if impact:
        query = query.filter(ComplianceChange.impact_level == impact)

    return query.limit(limit).all()


def get_high_impact_changes(session: Session, limit: int = 20) -> list[ComplianceChange]:
    """Get high-impact compliance changes."""
    return (
        session.query(ComplianceChange)
        .filter(ComplianceChange.impact_level == "HIGH")
        .order_by(ComplianceChange.retrieved_at.desc())
        .limit(limit)
        .all()
    )
