"""
Tests for the SauceDemo shopping cart via the inventory page.

Covers: adding a single item, adding multiple items, removing an item from
the inventory page, and verifying cart contents on the cart page.
"""

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


# Verifies that adding one item increments the cart badge count to 1.
def test_add_single_item(logged_in: InventoryPage):
    logged_in.add_to_cart("Sauce Labs Backpack")
    assert logged_in.get_cart_count() == 1


# Verifies that adding two items increments the cart badge count to 2.
def test_add_multiple_items(logged_in: InventoryPage):
    logged_in.add_to_cart("Sauce Labs Backpack")
    logged_in.add_to_cart("Sauce Labs Bike Light")
    assert logged_in.get_cart_count() == 2


# Verifies that removing an item from the inventory page resets the cart badge to 0.
def test_remove_item_from_inventory(logged_in: InventoryPage):
    logged_in.add_to_cart("Sauce Labs Backpack")
    logged_in.remove_from_cart("Sauce Labs Backpack")
    assert logged_in.get_cart_count() == 0


# Verifies that an item added from inventory actually appears on the cart page.
def test_cart_shows_correct_items(logged_in: InventoryPage, cart_page: CartPage):
    logged_in.add_to_cart("Sauce Labs Backpack")
    logged_in.go_to_cart()
    assert "Sauce Labs Backpack" in cart_page.get_item_names()
