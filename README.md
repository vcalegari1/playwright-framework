# Playwright Test Automation Framework — SauceDemo

A production-ready Python test automation framework for [saucedemo.com](https://www.saucedemo.com) with AI-powered failure analysis, Page Object Models, and CI/CD integration.

## Technologies

| Technology | Purpose |
|-----------|---------|
| **Python 3.12** | Programming language |
| **Playwright** | Cross-browser automation (Chromium, Firefox, WebKit) |
| **pytest** | Test runner and assertions |
| **Anthropic Claude API** | AI-powered failure analysis |
| **GitHub Actions** | CI/CD pipeline and automated testing |

## Features

- **Page Object Model (POM)** — Encapsulated page interactions for maintainable, scalable tests
- **AI-Powered Failure Analysis** — Claude analyzes test failures and suggests fixes in real-time
- **HTML Test Reports** — Self-contained, shareable test reports with screenshots and logs
- **Parallel Test Execution** — Run tests concurrently across multiple workers
- **CI/CD Pipeline** — Automated testing on every push/PR with GitHub Actions
- **Environment Configuration** — Flexible setup via `.env` files and environment variables

## Project Structure

```
playwright-framework/
├── tests/                      # Test modules (test_login.py, test_cart.py, etc.)
├── pages/                      # Page Object Models (LoginPage, InventoryPage, CartPage)
│   ├── login_page.py          # Locators and methods for login page interactions
│   ├── inventory_page.py       # Locators and methods for inventory/products page
│   ├── cart_page.py            # Locators and methods for shopping cart page
│   └── __init__.py             # Package initialization
├── fixtures/                   # Reusable pytest fixtures
│   └── __init__.py             # Package initialization
├── utils/                      # Utilities and configuration
│   ├── config.py               # Base URL, test user credentials, timeouts
│   ├── ai_helper.py            # Claude API integration for failure analysis and test data generation
│   └── __init__.py             # Package initialization
├── reports/                    # Generated HTML test reports (git-ignored)
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI/CD pipeline
├── conftest.py                 # Root pytest configuration and shared fixtures
├── pytest.ini                  # pytest discovery and CLI options
├── requirements.txt            # Python package dependencies
├── .env                        # Environment variables (git-ignored, local only)
├── .gitignore                  # Git ignore patterns
└── README.md                   # This file
```

## Setup

### Prerequisites

- Python 3.12 or later
- Git
- Virtual environment tool (venv)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/playwright-framework.git
   cd playwright-framework
   ```

2. **Create a Python virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Playwright browser binaries**
   ```bash
   playwright install chromium
   playwright install-deps chromium
   ```

6. **Create a `.env` file in the project root**
   ```bash
   cp .env.example .env  # or create manually
   ```
   Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
   ```

## Running Tests

### Run All Tests

```bash
pytest -v
```

### Run a Specific Test File

```bash
pytest tests/test_login.py -v
```

### Run a Specific Test

```bash
pytest tests/test_login.py::test_successful_login -v
```

### Run with Markers

```bash
# Run only login tests
pytest -m login -v

# Run only cart tests
pytest -m cart -v

# Run smoke tests
pytest -m smoke -v
```

### Run Tests in Parallel (4 workers)

```bash
pytest -n 4 -v
```

### Generate HTML Report

Reports are generated automatically. Open the report after a test run:

```bash
# After running tests
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

1. **Checks out** the latest code
2. **Sets up** Python 3.12 environment
3. **Installs** Python dependencies and Playwright browsers
4. **Runs** the full test suite in headless Chromium mode
5. **Uploads** the HTML report as a workflow artifact
6. **Analyzes** test failures using Claude AI (displays analysis in logs)

### Setting Up Secrets

To enable AI-powered failure analysis in CI:

1. Go to your repository **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your Anthropic API key (get it from [console.anthropic.com](https://console.anthropic.com))

### View Test Reports

After a workflow run:

1. Go to the workflow run details
2. Click **Artifacts** section
3. Download `html-report`
4. Open `report.html` in your browser

## Test Suite

| Test File | Description |
|-----------|-------------|
| `test_login.py` | Login page tests (valid/invalid credentials, locked users, empty fields) |
| `test_cart.py` | Shopping cart tests (add/remove items, verify cart contents) |

## Development

### Add a New Test

Create a new file in `tests/`:

```python
import pytest
from pages.inventory_page import InventoryPage

def test_new_scenario(logged_in: InventoryPage):
    """Description of what this test validates."""
    logged_in.add_to_cart("Sauce Labs Backpack")
    assert logged_in.get_cart_count() == 1
```

### Add a New Page Object

Create a new file in `pages/`:

```python
from playwright.sync_api import Page

class NewPage:
    SELECTOR = ".element"
    
    def __init__(self, page: Page):
        self.page = page
    
    def action(self):
        self.page.locator(self.SELECTOR).click()
```

### View AI Failure Analysis

When a test fails locally, Claude's analysis appears in the terminal output:

```
🤖 AI Analysis:
The test failed because the login button was not visible...
```

In CI, check the workflow logs for the same analysis.

## Troubleshooting

### `ANTHROPIC_API_KEY not found`

**Solution:** Create a `.env` file with your API key:
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Playwright browsers not found

**Solution:** Reinstall Playwright browsers:
```bash
playwright install chromium
playwright install-deps chromium
```

### Tests timeout in CI

**Solution:** Check `.github/workflows/ci.yml` and increase `DEFAULT_TIMEOUT` in `utils/config.py`.

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Write tests for new functionality
3. Run tests locally: `pytest -v`
4. Commit: `git commit -m "feat: add my feature"`
5. Push and open a pull request

## License

MIT License — see LICENSE file for details.

## Support

For issues, questions, or suggestions, open a GitHub issue or contact the team.
