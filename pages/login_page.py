# Page Object Model for the SauceDemo login page (https://www.saucedemo.com).
# Encapsulates locators and actions: fill credentials, click login, assert error messages.

from playwright.sync_api import Page
from utils.config import BASE_URL


class LoginPage:
    # Class variables (static in Java) — shared across all instances, defined at class level
    # These are like static final String fields in a Java class
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"
    ERROR_MESSAGE  = "[data-test='error']"

    # __init__ is Python's constructor (like LoginPage() in Java)
    # self is Python's version of 'this' in Java — refers to the instance
    def __init__(self, page: Page):
        # self.page stores the page object as an instance variable (like this.page in Java)
        self.page = page

    # Navigates the browser to the SauceDemo login page.
    def navigate(self):
        self.page.goto(BASE_URL)

    # Fills in the username and password fields then submits the login form.
    # Type hints (: str) declare parameter types; no modifier like Java's public/private needed
    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    # Returns the visible error banner text, or an empty string if no error is shown.
    # -> str is the return type hint (like public String getErrorMessage() in Java)
    def get_error_message(self) -> str:
        locator = self.page.locator(self.ERROR_MESSAGE)
        # This is a ternary expression: value_if_true if condition else value_if_false
        # In Java this would be: return locator.isVisible() ? locator.innerText() : ""
        return locator.inner_text() if locator.is_visible() else ""

    # Returns True when the login button is present and visible — confirms the page has loaded.
    def is_loaded(self) -> bool:
        return self.page.locator(self.LOGIN_BUTTON).is_visible()
