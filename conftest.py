# Root pytest configuration: shared fixtures available to all tests.
# Provides page-object fixtures, a pre-authenticated session, and browser configuration.

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import BASE_URL, USERS
from utils.ai_helper import analyze_failure


# Widens the default viewport to 1280×720 for all browser contexts in the session.
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # {**dict} unpacks the dictionary (like Java's Map.putAll or spread operator in JS)
    return {**browser_context_args, "viewport": {"width": 1280, "height": 720}}


# Provides a fresh browser page pointed at BASE_URL; closes the page after the test.
# This is similar to Java's @Before (setup) and @After (teardown), but uses 'yield' instead.
@pytest.fixture(scope="function")
def page(page: Page):  # Type hint ': Page' tells pytest the expected type (like Java <T> generics)
    page.goto(BASE_URL)
    yield page  # yield suspends here, runs the test, then resumes after the test ends
    page.close()  # This cleanup code runs after each test, similar to @After


# Provides a LoginPage instance bound to the current test's page.
# Return type hint '-> LoginPage' declares what type this function returns (like Java method signature)
@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


# Provides an InventoryPage instance bound to the current test's page.
@pytest.fixture(scope="function")
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


# Provides a CartPage instance bound to the current test's page.
@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


# Logs in as the standard user and returns an InventoryPage ready for the test to use.
@pytest.fixture(scope="function")
def logged_in(page: Page) -> InventoryPage:
    lp = LoginPage(page)
    # Dictionary access with square brackets (like Java Map.get()) retrieves the "standard" key
    lp.login(USERS["standard"]["username"], USERS["standard"]["password"])
    return InventoryPage(page)


# Pytest hook that runs after each test completes (like TestNG @AfterMethod or JUnit @After).
# Hooks are special callback functions that pytest calls automatically at key moments in the test lifecycle.
# This is similar to Java's TestListener or TestWatcher interfaces — pytest calls these functions automatically.
# report.when has three possible values: "setup" (before test), "call" (during test), "teardown" (after cleanup).
# We only care about "call" because that's when the actual test runs and can fail.
def pytest_runtest_logreport(report):
    """
    Called after each test phase completes. Used here to analyze test failures with Claude AI.

    Args:
        report: A TestReport object containing test execution details (like exception info, status, etc.)
    """
    # Check if this is a test failure during the "call" phase (when the test actually runs)
    # report.when == "call" ensures we only act on test execution, not setup/teardown failures
    # report.failed is a boolean; True means the test assertion failed or an exception was raised
    if report.when == "call" and report.failed:
        # Extract the test name from report.nodeid (like "tests/test_login.py::test_successful_login")
        # nodeid is the fully-qualified test path, suitable for identifying the test in logs/reports
        test_name = report.nodeid

        # Extract the error message from report.longreprtext (like Java's Throwable.getMessage())
        # longreprtext is the full formatted exception/assertion failure text that pytest displays
        # Use .get() like Java's Map.get() to safely retrieve it (returns None if not present)
        error_message = report.longreprtext or "No error message available"

        # Wrap the AI analysis in try/except so that API failures don't crash the test run
        # This is crucial for CI/CD reliability — if Claude API is down, tests should still complete
        try:
            # Call the AI analysis function (similar to calling any utility function)
            # analyze_failure returns a string with Claude's explanation of the failure
            analysis = analyze_failure(test_name, error_message)

            # Print the analysis with clear formatting so it's easy to spot in the test output
            # print() writes to stdout (like System.out.println() in Java)
            # The formatting uses emoji and newlines to make the output visually distinct
            print(f"\n🤖 AI Analysis:\n{analysis}\n")

        except Exception as e:
            # If the API call fails (network error, invalid API key, etc.), warn but don't crash
            # This is defensive programming — non-critical features shouldn't block the test run
            print(
                f"\n⚠️  AI Analysis failed: {str(e)}\n"
                f"   Make sure ANTHROPIC_API_KEY is set and valid in your .env file.\n"
            )
