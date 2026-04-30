# Page Object Model for the SauceDemo products/inventory page.
# Encapsulates locators and actions: sort items, add/remove from cart, navigate to cart.

from playwright.sync_api import Page


class InventoryPage:
    # Class variables (static in Java) — shared across all instances
    PRODUCT_LIST   = ".inventory_list"
    PRODUCT_NAMES  = ".inventory_item_name"
    CART_BADGE     = ".shopping_cart_badge"
    CART_ICON      = ".shopping_cart_link"

    # __init__ is Python's constructor; self is like Java's 'this'
    def __init__(self, page: Page):
        # self.page is an instance variable (like this.page = page in Java)
        self.page = page

    # Returns True when the inventory container is visible — confirms the page has loaded.
    def is_loaded(self) -> bool:
        return self.page.locator(self.PRODUCT_LIST).is_visible()

    # Returns a list of every product name string currently shown on the page.
    # list[str] is a type hint meaning "a list of strings" (Java would use List<String>)
    def get_product_names(self) -> list[str]:
        return self.page.locator(self.PRODUCT_NAMES).all_inner_texts()

    # Clicks the "Add to cart" button for the product whose name matches exactly.
    def add_to_cart(self, product_name: str):
        # SauceDemo button data-test IDs are derived from the product name:
        # "Sauce Labs Backpack" -> "add-to-cart-sauce-labs-backpack"
        slug = product_name.lower().replace(" ", "-")
        # f"..." is an f-string (formatted string literal) — like Java's String.format() or StringBuffer
        # In Java: String.format("[data-test='add-to-cart-%s']", slug)
        # In Python: f"[data-test='add-to-cart-{slug}']"
        self.page.locator(f"[data-test='add-to-cart-{slug}']").click()

    # Clicks the "Remove" button for the product whose name matches exactly.
    def remove_from_cart(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        # Another f-string: expressions inside {} are evaluated at runtime
        self.page.locator(f"[data-test='remove-{slug}']").click()

    # Returns the cart item count shown on the badge, or 0 when the badge is absent.
    def get_cart_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        # Ternary expression: in Java this would be: return badge.isVisible() ? Integer.parseInt(badge.innerText()) : 0
        # int() converts a string to an integer, like Java's Integer.parseInt()
        return int(badge.inner_text()) if badge.is_visible() else 0

    # Clicks the cart icon to navigate to the shopping cart page.
    def go_to_cart(self):
        self.page.locator(self.CART_ICON).click()
