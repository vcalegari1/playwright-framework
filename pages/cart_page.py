# Page Object Model for the SauceDemo shopping cart page.
# Encapsulates locators and actions: view cart items, remove items, proceed to checkout.

from playwright.sync_api import Page


class CartPage:
    # Class variables (static in Java) — shared across all instances
    CART_ITEMS               = ".cart_item"
    ITEM_NAMES               = ".inventory_item_name"
    CHECKOUT_BUTTON          = "[data-test='checkout']"
    REMOVE_BUTTON            = "[data-test^='remove-']"  # ^= is a CSS selector "starts-with" matcher
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"

    # __init__ is Python's constructor; self is like Java's 'this'
    def __init__(self, page: Page):
        # self.page is an instance variable (like this.page = page in Java)
        self.page = page

    # Returns True when the cart item list is present — confirms the cart page has loaded.
    def is_loaded(self) -> bool:
        # .first is like Selenium's findElements()[0] — grabs the first matching element
        return self.page.locator(self.CART_ITEMS).first.is_visible()

    # Returns a list of every item name string currently in the cart.
    # list[str] is a type hint for "list of strings" (Java: List<String>)
    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    # Clicks the Remove button for the cart item whose name matches exactly.
    def remove_item(self, item_name: str):
        slug = item_name.lower().replace(" ", "-")
        # f-string (formatted string literal) — like Java's String.format()
        self.page.locator(f"[data-test='remove-{slug}']").click()

    # Clicks Checkout to proceed to the customer information form.
    def checkout(self):
        self.page.locator(self.CHECKOUT_BUTTON).click()

    # Clicks Continue Shopping to return to the inventory page without checking out.
    def continue_shopping(self):
        self.page.locator(self.CONTINUE_SHOPPING_BUTTON).click()

    # Returns the number of items currently in the cart.
    # .count() is similar to findElements().size() in Selenium
    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()
