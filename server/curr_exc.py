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
    transport="stdio"  # Set to stdio for Claude Desktop compatibility
)

# Constants
# Get API key from environment variable
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
if not API_KEY:
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
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            if data.get("result") == "error":
                logger.error(f"API Error: {data.get('error-type')}")
                return None
            return data
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error: {str(e)}")
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
    data = await make_exchange_request(url)

    if not data:
        return "Unable to fetch list of supported currencies. Please check if your API key is valid."

    if data.get("result") != "success":
        error_type = data.get("error-type", "unknown")
        return f"Error: {error_type}"

    codes = data.get("supported_codes", [])    
    currencies = [f"{code} - {name}" for code, name in codes]

    return "\n".join(sorted(currencies))

if __name__ == "__main__":
    logger.info("Starting currency exchange server...")
    mcp.run(transport="stdio")  # Use stdio transport for Claude Desktop
    logger.info("Server is running. Press Ctrl+C to stop.")

# Make sure the mcp object is available at module level
__all__ = ["mcp"]
