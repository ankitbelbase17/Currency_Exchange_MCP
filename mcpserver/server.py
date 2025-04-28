from typing import Any
import httpx
import logging
import os
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP(
    name="currency-exchange",
    host="0.0.0.0",  # Listen on all interfaces
    port=8004,  # Use port 8004
)

# Constants
# Get API key from environment variable, with a placeholder for documentation
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "your_api_key_here")
if API_KEY == "your_api_key_here":
    raise ValueError("Please set the EXCHANGE_RATE_API_KEY environment variable. Get your API key from https://www.exchangerate-api.com/")

EXCHANGE_API_BASE = f"https://v6.exchangerate-api.com/v6/{API_KEY}"
USER_AGENT = "currency-exchange-app/1.0"

async def make_exchange_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Exchange Rate API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        try:
            print(f"Making request to: {url}")  # Log the URL being requested
            print(f"Using API key: {API_KEY}")  # Log the API key being used
            response = await client.get(url, headers=headers, timeout=30.0)
            print(f"Response status: {response.status_code}")  # Log the status code
            response.raise_for_status()
            data = response.json()
            print(f"Response data: {data}")  # Log the response data
            if data.get("result") == "error":
                error_type = data.get("error-type", "unknown")
                error_info = data.get("error-info", "no additional info")
                logger.error(f"API Error: {error_type} - {error_info}")
                return None
            return data
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

@mcp.tool()
async def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Get the current exchange rate between two currencies.

    Args:
        from_currency: The currency code to convert from (e.g., 'USD')
        to_currency: The currency code to convert to (e.g., 'EUR')
    """
    url = f"{EXCHANGE_API_BASE}/pair/{from_currency.upper()}/{to_currency.upper()}"
    data = await make_exchange_request(url)

    if not data:
        return "Unable to fetch exchange rate. Please check if your API key is valid."

    if data.get("result") != "success":
        error_type = data.get("error-type", "unknown")
        return f"Error: {error_type}"

    rate = data.get("conversion_rate")
    if rate is None:
        return "Exchange rate not available."

    return f"💱 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"

@mcp.tool()
async def list_supported_currencies() -> str:
    """List all supported currencies."""
    url = f"{EXCHANGE_API_BASE}/codes"
    print(f"Requesting currency codes from: {url}")  # Add logging
    data = await make_exchange_request(url)

    if not data:
        return "Unable to fetch list of supported currencies. Please check if your API key is valid."

    if data.get("result") != "success":
        error_type = data.get("error-type", "unknown")
        error_info = data.get("error-info", "no additional info")
        print(f"API Error: {error_type} - {error_info}")  # Add logging
        return f"Error: {error_type}"

    codes = data.get("supported_codes", [])
    if not codes:
        print("No currency codes returned from API")  # Add logging
        return "No currency data available."

    # Format the currencies nicely
    currencies = [f"{code} - {name}" for code, name in sorted(codes)]
    print(f"Found {len(currencies)} supported currencies")  # Add logging
    return "\n".join(currencies)


# Run the server
if __name__ == "__main__":
    try:
        # Force SSE mode for HTTP access
        print("Starting currency exchange server in SSE mode...")
        print(f"Server will be available at: http://localhost:8004")
        mcp.run(transport="sse")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f"Server error: {str(e)}")  # Additional error logging
        raise

# Make sure the mcp object is available at module level
__all__ = ["mcp"]
