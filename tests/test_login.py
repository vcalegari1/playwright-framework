"""
Tests for the SauceDemo login page.

Covers: successful login, locked-out user error, empty credential validation,
and invalid password rejection.
"""

import pytest
from pages.login_page import LoginPage
from utils.config import USERS


# Verifies that a valid standard user is redirected to the inventory page after login.
def test_successful_login(login_page: LoginPage):
    login_page.login(
        USERS["standard"]["username"],
        USERS["standard"]["password"],
    )
    assert "inventory" in login_page.page.url


# Verifies that the locked-out user sees an appropriate error message instead of logging in.
def test_locked_out_user(login_page: LoginPage):
    login_page.login(
        USERS["locked"]["username"],
        USERS["locked"]["password"],
    )
    assert "locked out" in login_page.get_error_message().lower()


# Verifies that submitting the form with no credentials triggers a validation error.
def test_empty_credentials(login_page: LoginPage):
    login_page.login("", "")
    assert login_page.get_error_message() != ""


# Verifies that a correct username paired with a wrong password is rejected with an error.
def test_invalid_password(login_page: LoginPage):
    login_page.login(USERS["standard"]["username"], "wrong_password")
    assert login_page.get_error_message() != ""
