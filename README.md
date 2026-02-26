# CXC Global Compliance Intelligence

[![CI](https://github.com/farbotkol/compliencechange/actions/workflows/ci.yml/badge.svg)](https://github.com/farbotkol/compliencechange/actions/workflows/ci.yml)

**Production-quality compliance and legislative change monitoring for CXC Global**

## 🎯 What This Application Does

CXC Global Compliance Intelligence is an automated monitoring system that continuously tracks compliance, regulatory, and legislative changes relevant to CXC Global's business operations, including:

- **Employer of Record (EOR)** services
- **Agent/Contractor of Record (AOR/COR)** services  
- **Contractor classification & misclassification** regulations
- **Global payroll, tax withholding, and social security** requirements
- **Employment law** (wages, benefits, termination, leave)
- **Data privacy & data residency** (GDPR and similar laws)
- **Cross-border workforce** regulations
- **MSP / contingent workforce** governance

The system monitors only **publicly available sources** and clearly distinguishes:

- ✅ **Confirmed legal changes** (enacted laws)
- ⚠️ **Proposed / draft legislation**
- ℹ️ **Regulatory guidance / enforcement updates**

## 🌍 Supported Jurisdictions

Currently monitoring compliance changes from:

- 🇦🇺 **Australia** (Fair Work Ombudsman, ATO)
- 🇪🇺 **European Union** (European Commission, EDPB)
- 🇬🇧 **United Kingdom** (HMRC, Department for Business and Trade)
- 🇺🇸 **United States** (DOL, IRS)
- 🌐 **International** (ILO, OECD)

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/farbotkol/compliencechange.git
cd compliencechange
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python -m app.cli init-db
```

### Running a Scan

Execute a compliance scan across all jurisdictions:

```bash
python -m app.cli run-scan
```

This will:
- Fetch compliance changes from authoritative sources
- Score each change for relevance and impact
- Store results with evidence hashes (idempotent)
- Display a summary of findings

### Starting the Web Application

Launch the API and web UI:

```bash
uvicorn app.main:app --reload
```

Then open your browser to: **http://localhost:8000**

## 📊 Viewing Compliance Changes

### Web UI

Navigate to http://localhost:8000 to:
- View recent compliance changes
- Filter by country, legal domain, or impact level
- See clear badges for "Enacted" vs "Proposed" changes
- Access source URLs for verification

### API Endpoints

The application exposes a REST API:

```bash
# Health check
GET http://localhost:8000/health

# Latest changes
GET http://localhost:8000/changes/latest

# Filtered changes
GET http://localhost:8000/changes?country=AU&domain=employment_law&impact=HIGH

# Specific change
GET http://localhost:8000/changes/{id}

# Trigger a scan
POST http://localhost:8000/run-scan

# High-impact alerts
GET http://localhost:8000/alerts/high-impact

# Export to CSV
GET http://localhost:8000/export/changes.csv
```

### Example API Response

```json
{
  "id": 1,
  "jurisdiction": "Australia",
  "country_code": "AU",
  "legal_domain": "employment_law",
  "service_impacted": "COR, AOR",
  "change_type": "REGULATORY_UPDATE",
  "title": "Fair Work Commission updates on contractor classification",
  "summary": "The Fair Work Ombudsman has published updated guidance...",
  "source_url": "https://www.fairwork.gov.au/...",
  "publisher": "Fair Work Ombudsman – AU",
  "published_date": "2024-01-15T00:00:00",
  "effective_date": null,
  "retrieved_at": "2024-02-26T03:00:00",
  "impact_level": "HIGH",
  "evidence_text": "Fair Work Ombudsman guidance: Independent contractors...",
  "evidence_sha256": "a1b2c3..."
}
```

## 🏗️ Architecture

### Tech Stack

- **Python 3.12** - Modern Python features
- **FastAPI** - High-performance async API framework
- **SQLAlchemy + Alembic** - ORM and database migrations
- **SQLite** - Default database (easily swappable)
- **httpx + BeautifulSoup** - HTTP client and HTML parsing
- **Jinja2** - Server-side templating

### Project Structure

```
cxc-global-compliance-intelligence/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── api.py               # FastAPI routes and endpoints
│   ├── models.py            # SQLAlchemy database models
│   ├── schema.py            # Pydantic response schemas
│   ├── relevance.py         # Rule-based relevance scoring
│   ├── db.py                # Database utilities
│   ├── cli.py               # CLI commands
│   └── collectors/          # Jurisdiction-specific collectors
│       ├── base.py          # Base collector class
│       ├── australia.py
│       ├── european_union.py
│       ├── united_kingdom.py
│       ├── united_states.py
│       └── international.py
├── data/
│   └── sources.yaml         # Data source configuration
├── tests/
│   ├── conftest.py          # Test configuration
│   ├── test_api.py          # API endpoint tests
│   ├── test_collectors.py   # Collector tests
│   ├── test_database.py     # Database and idempotency tests
│   └── test_relevance.py    # Relevance scoring tests
├── templates/
│   └── index.html           # Web UI template
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## 🔍 How It Works

### 1. Collectors

Each jurisdiction has a dedicated collector that:
- Knows its authoritative public sources
- Fetches latest compliance updates
- Parses and extracts relevant information
- Emits structured `ComplianceChangeData` objects

### 2. Relevance Scoring

A rule-based engine scores each change:

**High Impact:**
- Contractor misclassification laws
- EOR/AOR regulatory changes
- Cross-border employment requirements
- Payroll/tax withholding updates
- GDPR-style data privacy laws

**Medium Impact:**
- Wage and hour updates
- General employment law changes
- Reporting requirements

**Low Impact:**
- Administrative guidance
- Form/template updates

### 3. Evidence & Auditability

Every compliance change includes:
- **Source URL** - Direct link to authoritative source
- **Publisher** - Who issued the change
- **Dates** - Published and effective dates
- **Evidence excerpt** - Up to 1,000 characters
- **SHA-256 hash** - Ensures idempotency (no duplicates)

### 4. Idempotency

Running the same scan multiple times will NOT create duplicates. The system uses evidence hashes to detect and skip existing records.

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_relevance.py
```

## 🔧 Development

### Linting

```bash
ruff check .
```

### Docker

Build and run with Docker:

```bash
# Build image
docker build -t cxc-compliance .

# Run container
docker run -p 8000:8000 cxc-compliance

# Or use docker-compose
docker-compose up
```

## 📋 CI/CD

GitHub Actions automatically runs on every push:

1. ✅ Lints code with `ruff`
2. ✅ Runs full test suite with `pytest`
3. ✅ Generates coverage report

See [.github/workflows/ci.yml](.github/workflows/ci.yml) for configuration.

## ⚠️ Important Disclaimer

**This tool provides informational monitoring only and does not constitute legal advice.**

The compliance intelligence gathered by this system is for informational purposes. Always consult with qualified legal professionals for specific compliance requirements and legal interpretations.

This application:
- ✅ Monitors publicly available sources
- ✅ Provides factual summaries
- ✅ Links to authoritative sources
- ❌ Does NOT provide legal advice
- ❌ Does NOT scrape paywalled content
- ❌ Does NOT guarantee completeness

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 🔒 Security

See [SECURITY.md](SECURITY.md) for security policies and reporting vulnerabilities.

## 📄 License

Copyright © 2024 CXC Global. All rights reserved.

---

**Built with ❤️ for CXC Global's compliance team**