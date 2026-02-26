"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "database" in data


def test_root_endpoint():
    """Test the root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_changes_latest():
    """Test getting latest changes."""
    response = client.get("/changes/latest")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_changes_with_filters():
    """Test getting changes with filters."""
    response = client.get("/changes?country=AU&impact=HIGH")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_changes_limit():
    """Test limit parameter."""
    response = client.get("/changes/latest?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 10


def test_get_high_impact_alerts():
    """Test getting high-impact alerts."""
    response = client.get("/alerts/high-impact")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_export_csv():
    """Test CSV export endpoint."""
    response = client.get("/export/changes.csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "Content-Disposition" in response.headers


def test_get_change_not_found():
    """Test getting a non-existent change."""
    response = client.get("/changes/999999")
    assert response.status_code == 404
