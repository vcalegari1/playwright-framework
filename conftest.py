# Root pytest configuration: shared fixtures available to all tests.
# Provides page-object fixtures, a pre-authenticated session, and browser configuration.

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import BASE_URL, USERS


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
