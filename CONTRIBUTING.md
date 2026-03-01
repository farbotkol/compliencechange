# Contributing to CXC Global Compliance Intelligence

Thank you for your interest in contributing to CXC Global Compliance Intelligence!

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/compliencechange.git
   cd compliencechange
   ```
3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

1. Install Python 3.12 or higher
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Initialize the database:
   ```bash
   python -m app.cli init-db
   ```

## 📝 Coding Standards

### Code Style

We use **Ruff** for linting and code formatting:

```bash
# Check code
ruff check .

# Auto-fix issues
ruff check . --fix
```

### Code Quality

- Write clear, self-documenting code
- Add docstrings to all functions and classes
- Follow PEP 8 naming conventions
- Keep functions focused and single-purpose
- Use type hints where appropriate

### Testing

All contributions must include tests:

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Aim for >80% code coverage
```

#### Test Guidelines

- Write tests for new features
- Update tests when modifying existing code
- Use descriptive test names: `test_should_do_something_when_condition()`
- Use fixtures for common test setup (see `tests/conftest.py`)
- Mock external HTTP calls (don't hit real APIs in tests)

## 📦 Adding New Collectors

To add a new jurisdiction collector:

1. Create `app/collectors/your_jurisdiction.py`
2. Inherit from `BaseCollector`
3. Implement `get_sources()` and `collect()` methods
4. Add tests in `tests/test_collectors.py`
5. Add HTML fixtures in `tests/fixtures/` for testing

Example:

```python
from app.collectors.base import BaseCollector, ComplianceChangeData

class YourJurisdictionCollector(BaseCollector):
    def get_sources(self):
        return [
            {
                "url": "https://example.gov/updates",
                "name": "Government Agency",
                "type": "employment_law"
            }
        ]
    
    def collect(self):
        # Implement collection logic
        changes = []
        # ... fetch and parse ...
        return changes
```

## 🔍 Relevance Scoring

When adding new high-impact keywords to `app/relevance.py`:

1. Ensure they're directly relevant to CXC's business
2. Add corresponding tests in `tests/test_relevance.py`
3. Document why the keyword indicates high impact

## 🧪 Running Quality Checks

Before submitting a PR:

```bash
# 1. Lint code
ruff check .

# 2. Run all tests
pytest

# 3. Check test coverage
pytest --cov=app --cov-report=html

# 4. Manual testing
python -m app.cli run-scan
uvicorn app.main:app --reload
```

## 📬 Submitting Changes

1. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "feat: add support for Canada compliance monitoring"
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference any related issues
   - Ensure CI checks pass

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

## 🐛 Reporting Bugs

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or error messages

## 💡 Suggesting Features

Feature requests are welcome! Please:

- Check if it's already been suggested
- Explain the use case
- Describe the expected behavior
- Consider implementation implications

## 🔒 Security

**Do not** open public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for responsible disclosure.

## ⚖️ Legal Compliance

When contributing:

- Only use publicly available sources
- Do not scrape paywalled or login-required content
- Do not include legal advice in summaries
- Clearly mark proposed vs enacted legislation
- Include source URLs and evidence for all changes

## 📚 Documentation

When adding features:

- Update README.md if user-facing
- Add docstrings to new code
- Update API documentation if endpoints change
- Add examples for complex features

## ❓ Questions?

If you have questions:

- Check existing documentation
- Review closed issues/PRs
- Open a discussion on GitHub

---

Thank you for contributing to making compliance monitoring better! 🙌
