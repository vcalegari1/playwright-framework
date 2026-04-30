# Playwright Test Automation Framework — SauceDemo

End-to-end test suite for [saucedemo.com](https://www.saucedemo.com) built with Python, Playwright, and pytest.

## Stack

| Tool | Purpose |
|------|---------|
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [pytest](https://docs.pytest.org/) | Test runner & assertions |
| [pytest-html](https://pytest-html.readthedocs.io/) | HTML test reports |
| [pytest-xdist](https://pytest-xdist.readthedocs.io/) | Parallel test execution |
| [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) | AI-assisted test utilities |

## Setup

```bash
pip install -r requirements.txt
playwright install
```

## Running Tests

```bash
# All tests
pytest

# Smoke tests only
pytest -m smoke

# Headless (CI)
pytest --headed=false

# Parallel (4 workers)
pytest -n 4
```

## Project Structure

```
playwright-framework/
├── tests/               # Test files (test_*.py)
├── pages/               # Page Object Models
├── fixtures/            # Reusable pytest fixtures
├── utils/               # Config, helpers, AI utilities
├── reports/             # Generated HTML reports
├── .github/workflows/   # CI/CD pipelines
├── conftest.py          # Root shared fixtures
├── pytest.ini           # pytest configuration
└── requirements.txt     # Python dependencies
```
