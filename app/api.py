"""FastAPI application for compliance monitoring."""
import csv
import io
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.cli import run_scan as cli_run_scan
from app.db import get_db_session, get_high_impact_changes, get_latest_changes
from app.models import ComplianceChange, init_db
from app.schema import (
    ComplianceChangeResponse,
    HealthResponse,
    ScanTriggerResponse,
)

# Initialize database on startup
init_db()

app = FastAPI(
    title="CXC Global Compliance Intelligence",
    description="Compliance and legislative change monitoring system",
    version="0.1.0",
)

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint with UI."""
    session = get_db_session()
    changes = get_latest_changes(session, limit=20)
    session.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "changes": changes,
            "title": "CXC Global Compliance Intelligence",
        },
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        database="connected",
    )


@app.get("/changes/latest", response_model=List[ComplianceChangeResponse])
async def get_changes_latest(limit: int = Query(50, le=100)):
    """Get latest compliance changes."""
    session = get_db_session()
    changes = get_latest_changes(session, limit=limit)
    session.close()
    return changes


@app.get("/changes", response_model=List[ComplianceChangeResponse])
async def get_changes(
    country: Optional[str] = None,
    domain: Optional[str] = None,
    impact: Optional[str] = None,
    limit: int = Query(50, le=100),
):
    """Get compliance changes with filters."""
    session = get_db_session()
    changes = get_latest_changes(session, limit=limit, country=country, domain=domain, impact=impact)
    session.close()
    return changes


@app.get("/changes/{change_id}", response_model=ComplianceChangeResponse)
async def get_change(change_id: int):
    """Get specific compliance change by ID."""
    session = get_db_session()
    change = session.query(ComplianceChange).filter(ComplianceChange.id == change_id).first()
    session.close()
    if not change:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Change not found")
    return change


@app.post("/run-scan", response_model=ScanTriggerResponse)
async def trigger_scan():
    """Trigger a compliance scan."""
    # Note: In production, this should be async/background task
    cli_run_scan()
    return ScanTriggerResponse(
        message="Scan completed",
        scan_id=1,  # Should return actual scan_id
    )


@app.get("/alerts/high-impact", response_model=List[ComplianceChangeResponse])
async def get_high_impact_alerts(limit: int = Query(20, le=100)):
    """Get high-impact compliance alerts."""
    session = get_db_session()
    changes = get_high_impact_changes(session, limit=limit)
    session.close()
    return changes


@app.get("/export/changes.csv")
async def export_changes_csv(
    country: Optional[str] = None,
    domain: Optional[str] = None,
    impact: Optional[str] = None,
):
    """Export compliance changes as CSV."""
    session = get_db_session()
    changes = get_latest_changes(session, limit=1000, country=country, domain=domain, impact=impact)
    session.close()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        "ID", "Jurisdiction", "Country Code", "Legal Domain", "Service Impacted",
        "Change Type", "Title", "Summary", "Source URL", "Publisher",
        "Published Date", "Effective Date", "Retrieved At", "Impact Level"
    ])

    # Write data
    for change in changes:
        writer.writerow([
            change.id,
            change.jurisdiction,
            change.country_code,
            change.legal_domain,
            change.service_impacted,
            change.change_type,
            change.title,
            change.summary,
            change.source_url,
            change.publisher,
            change.published_date,
            change.effective_date,
            change.retrieved_at,
            change.impact_level,
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=compliance_changes.csv"}
    )
