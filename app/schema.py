"""Pydantic schemas for API."""
from datetime import datetime

from pydantic import BaseModel


class ComplianceChangeResponse(BaseModel):
    """Response schema for compliance changes."""

    id: int
    jurisdiction: str
    country_code: str
    legal_domain: str
    service_impacted: str | None
    change_type: str
    title: str
    summary: str
    source_url: str
    publisher: str
    published_date: datetime | None
    effective_date: datetime | None
    retrieved_at: datetime
    impact_level: str
    evidence_text: str
    evidence_sha256: str

    class Config:
        from_attributes = True


class ScanRunResponse(BaseModel):
    """Response schema for scan runs."""

    id: int
    start_time: datetime
    end_time: datetime | None
    items_found: int
    failures: str | None
    status: str

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Response schema for health check."""

    status: str
    version: str
    database: str


class ScanTriggerResponse(BaseModel):
    """Response schema for scan trigger."""

    message: str
    scan_id: int
