# AI-assisted utilities: generate test data, analyze failures, and suggest improvements.
# Integrates with the Claude API (Anthropic SDK) to add AI capabilities to the test framework.

# Load environment variables from .env file (like Java System.getenv() but reads from a file first)
from dotenv import load_dotenv
from pathlib import Path

# Standard library imports
import os
import json

# Third-party imports
from anthropic import Anthropic

# Find the .env file relative to this file's location (like Java's ClassLoader.getResource())
# Path(__file__) gives the absolute path to ai_helper.py itself
# .parent goes up one level to utils/ directory
# .parent again goes up to the project root where .env lives
# Using __file__ ensures we find .env regardless of where pytest is run from (cwd-independent)
# This is better than relative paths like "../.env" which break if you cd into a subdirectory
dotenv_path = Path(__file__).parent.parent / ".env"

# Load environment variables from the .env file (like Java System.getenv() but reads from a file)
# dotenv_path points to the explicit file location (not just the current working directory)
# override=True ensures .env values override environment variables (like Java System.setProperty)
load_dotenv(dotenv_path=dotenv_path, override=True)

# Retrieve API key from environment variables (like Java System.getProperty or System.getenv)
# os.getenv(key, default) returns the environment variable value, or default if not found
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Validate that the API key exists — fail fast if it's missing (like Java's null check)
# Raising an exception here prevents cryptic API errors downstream
if not ANTHROPIC_API_KEY:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY not found in environment. "
        "Add it to .env or export ANTHROPIC_API_KEY=sk-ant-... in your shell."
    )

# Initialize the Anthropic client (like creating a WebDriver instance in Selenium)
# The client is reused across function calls for efficiency
client = Anthropic()


# Analyzes a pytest test failure and returns a human-readable explanation from Claude.
# Takes the test name and error message, then asks Claude what went wrong and how to fix it.
def analyze_failure(test_name: str, error_message: str) -> str:
    """
    Sends a test failure to Claude for analysis.

    Args:
        test_name: Name of the failing test (e.g., "test_login_with_empty_password").
        error_message: The pytest assertion error or exception message.

    Returns:
        A string containing Claude's analysis of the failure and suggested fixes.
    """
    # Construct a detailed prompt for Claude (like building a request body for an API call)
    # The prompt includes context and structured questions to guide Claude's response
    prompt = f"""
You are a test automation expert. Analyze this pytest test failure and explain:
1. What went wrong?
2. What is the likely root cause?
3. What should the developer check or fix?

Test Name: {test_name}
Error Message: {error_message}

Provide a clear, concise explanation in plain English. Focus on actionable advice.
"""

    # Call the Claude API using the Anthropic SDK (similar to making an HTTP POST request)
    # This is a synchronous call — it blocks until Claude responds (no async/await here)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Use the fast Haiku model for speed
        max_tokens=1024,  # Limit response length (like a timeout on an HTTP request)
        messages=[
            {
                # Each message has a "role" (user/assistant) — like request/response in HTTP
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract the text response from Claude's message object (like parsing JSON from an API response)
    # message.content is a list of content blocks; [0] gets the first block, .text gets the text field
    return message.content[0].text


# Generates realistic test user data as JSON for a given test context.
# Asks Claude to create test data that matches the context (e.g., valid/invalid users, edge cases).
def generate_test_data(context: str) -> dict:
    """
    Asks Claude to generate test user data as JSON.

    Args:
        context: Description of what test data is needed (e.g., "locked_out user for login tests").

    Returns:
        A dictionary (parsed JSON) containing the generated test data.
    """
    # Build a prompt asking Claude to generate JSON test data
    # Specifying JSON format helps Claude structure the response in a parseable way
    prompt = f"""
You are a test data generator. Create realistic test user data as JSON for this context:
{context}

Return ONLY valid JSON (no markdown, no extra text). The JSON must be parseable by Python's json.loads().
Include fields like username, password, email, and any other relevant attributes.
"""

    # Call Claude API (same process as analyze_failure: send message, get response)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract the text from Claude's response
    response_text = message.content[0].text

    # Parse the JSON string into a Python dictionary (like JsonObject in Java)
    # json.loads(string) deserializes JSON text into a dict (opposite of json.dumps/serialize)
    # This may raise json.JSONDecodeError if Claude's response is not valid JSON
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        # If Claude's response is not valid JSON, provide a helpful error message
        # This is like try/catch for parsing errors in Java
        raise ValueError(
            f"Claude's response was not valid JSON. Response: {response_text}"
        ) from e
