# Central configuration: base URL, credentials, timeouts, and environment settings.
# Values are read from environment variables with sensible defaults for local development.

# Module-level constant (like public static final in Java)
BASE_URL = "https://www.saucedemo.com"

# Dictionary literal (like Java Map<String, Map<String, String>>) with nested dictionaries
# This is equivalent to: Map<String, Map<String, String>> USERS = new HashMap<>();
# USERS.put("standard", new HashMap<>(...))
# In Python, dictionaries use {} and key:value pairs (like JSON)
USERS = {
    # Each key ("standard", "locked", etc.) maps to a nested dictionary of credentials
    # Accessing: USERS["standard"]["username"] gets "standard_user"
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked":   {"username": "locked_out_user", "password": "secret_sauce"},
    "problem":  {"username": "problem_user", "password": "secret_sauce"},
    "perf":     {"username": "performance_glitch_user", "password": "secret_sauce"},
}

# Integer with numeric separator 10_000 (equivalent to 10000)
# Python 3.6+ allows underscores in numeric literals for readability (like Java 1.7+ does too)
# In Java: final int DEFAULT_TIMEOUT = 10_000; (same syntax!)
DEFAULT_TIMEOUT = 10_000  # milliseconds
