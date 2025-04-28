

import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8004.

To run the server:
python server.py
"""

async def main():
    try:
        # Connect to the server using SSE
        print("Connecting to server at http://localhost:8004/sse...")
        async with sse_client("http://localhost:8004/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                await session.initialize()

                # List available tools
                tools_result = await session.list_tools()
                print("\nAvailable tools:")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Call get_exchange_rate tool
                result = await session.call_tool(
                    "get_exchange_rate",
                    arguments={"from_currency": "INR", "to_currency": "USD"}
                )
                print(f"\nExchange rate INR to USD: {result.content[0].text}")

                # Call list_supported_currencies tool
                result = await session.call_tool("list_supported_currencies", arguments={})
                print("\nSupported currencies (first 10):")
                for line in result.content[0].text.splitlines()[:10]:
                    print(line)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())