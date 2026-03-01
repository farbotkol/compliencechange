"""Database models for compliance monitoring."""
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class ChangeType(str, Enum):
    """Types of compliance changes."""

    ENACTED_LAW = "ENACTED_LAW"
    REGULATORY_UPDATE = "REGULATORY_UPDATE"
    COURT_DECISION = "COURT_DECISION"
    PROPOSED_LEGISLATION = "PROPOSED_LEGISLATION"
    CONSULTATION = "CONSULTATION"
    GUIDANCE = "GUIDANCE"


class ImpactLevel(str, Enum):
    """Impact level for CXC services."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ComplianceChange(Base):
    """Model for storing compliance and legislative changes."""

    __tablename__ = "compliance_changes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jurisdiction = Column(String(200), nullable=False, index=True)
    country_code = Column(String(10), nullable=False, index=True)
    legal_domain = Column(String(100), nullable=False, index=True)
    service_impacted = Column(String(100), nullable=True)
    change_type = Column(String(50), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    source_url = Column(String(1000), nullable=False)
    publisher = Column(String(200), nullable=False)
    published_date = Column(DateTime, nullable=True)
    effective_date = Column(DateTime, nullable=True)
    retrieved_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    impact_level = Column(String(20), nullable=False, index=True)
    evidence_text = Column(Text, nullable=False)
    evidence_sha256 = Column(String(64), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f"<ComplianceChange {self.id}: {self.title[:50]}>"


class ScanRun(Base):
    """Model for tracking scan executions."""

    __tablename__ = "scan_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    items_found = Column(Integer, default=0)
    failures = Column(Text, nullable=True)
    status = Column(String(20), default="running")

    def __repr__(self):
        return f"<ScanRun {self.id}: {self.status}>"


# Database setup
def get_engine(database_url: str = "sqlite:///compliance.db"):
    """Create database engine."""
    return create_engine(database_url, echo=False)


def get_session_maker(engine):
    """Create session maker."""
    return sessionmaker(bind=engine)


def init_db(database_url: str = "sqlite:///compliance.db"):
    """Initialize database with tables."""
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)
    return engine
