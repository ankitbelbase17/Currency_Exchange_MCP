import asyncio
import nest_asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Apply nest_asyncio to allow running in interactive environments
nest_asyncio.apply()

async def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(script_dir, "server.py")

    print(f"Script directory: {script_dir}")
    print(f"Server script path: {server_script}")

    # Define server parameters with full path
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=[server_script],  # Full path to the server script
        cwd=script_dir,  # Set working directory to the script's directory
    )

    try:
        print("Starting server and connecting...")
        # Connect to the server
        print("Creating stdio client...")
        async with stdio_client(server_params) as (read_stream, write_stream):
            print("Connected to server, creating session...")
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                print("Initializing connection...")
                await session.initialize()
                print("Connection initialized successfully")

                # List available tools
                print("\nListing available tools...")
                tools_result = await session.list_tools()
                print("Available tools:")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Get exchange rate between INR and USD
                print("\nGetting exchange rate for INR to USD:")
                result = await session.call_tool(
                    "get_exchange_rate",
                    arguments={"from_currency": "INR", "to_currency": "USD"}
                )
                print(f"Exchange rate: {result.content[0].text}")

                # List supported currencies
                print("\nGetting list of supported currencies:")
                result = await session.call_tool("list_supported_currencies", arguments={})
                print("\nSupported currencies (first 10):")
                for line in result.content[0].text.splitlines()[:10]:
                    print(line)

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(main())
